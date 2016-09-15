;(function($, window, document, undefined) {
    'use strict';

    var CONST = {
        maxNumbComparisons: 5,
        add: 0,
        remove: 1
    }
    /* Datatable functionality */
    var DataTable = {
        initVariables: function() {
            this.frameworkTable = null;
        },

        cacheElements: function() {
            this.$modalContainer = $("#addFrameworkModal");
            this.$frameworkTable = $("#addFrameworksTable");
            this.$filterFieldContainer = $('#addFrameworksTable_filter');
            this.$filterField = $('#addFrameworksTable_filter').find(':input');
        },

        init: function($frameworkTable) {
            this.initVariables();
            this.initTable($frameworkTable);
            this.cacheElements();
            this.cleanMarkup();
            this.bindEvents();
            this.hideCurrentFrameworks(CF.currentFrameworks);
        },

        initTable: function($frameworkTable) {
            this.frameworkTable = $frameworkTable.DataTable({
                ajax: {
                    url: '../php/testThumbFrameworks.php',
                    dataSrc: "frameworks"
                },
                "columnDefs": [
                    { "visible": false, "targets": 1 }  // hide second column
                ],
                columns: [
                    {
                        data: 'framework',
                        "type": "html",
                        render: function (data, type, row) {
                            if (type ==='display') {
                                var thumbs = "";
                                thumbs = '<span class="thumb-framework"><img src="' + row.thumb_img + '" alt=""/></span> \
							              <span class="glyphicon glyphicon-plus pull-right thumb-add"></span> \
							              <span class="thumb-title">' + data + '</span> \
							              <span class="thumb-status ' + row.status.toLowerCase() + '">' + row.status + '</span>';
                                return thumbs;
                            } else return '';
                        }
                    },
                    {data:'framework'}  //Must provide second column in order for search to work...
                ],
                language: {
                    search: "<i class='glyphicon glyphicon-search modal-search-feedback'></i>",
                    searchPlaceholder: "Search by framework name...",
                    zeroRecords: "No Frameworks found. Please try another search term."
                },
                "sAutoWidth": false,
                "iDisplayStart ": 6,
                "iDisplayLength": 6,
                "lengthChange": false,
                "bInfo": false, // hide showing entries
            });
        },

        cleanMarkup: function() {
            this.$filterFieldContainer.removeClass('dataTables_filter');
            this.$filterFieldContainer.find("input").addClass("modal-search");
            this.$frameworkTable.addClass("table table-hover"); //add bootstrap class
            this.$frameworkTable.css("width","100%");
        },

        bindEvents: function() {
            var that = this;
            this.$modalContainer.on('shown.bs.modal', function (){
                // On modal overlay shown focus the search field
                that.$filterField.focus();
            });

            this.$frameworkTable.find('tbody').on('click', 'tr', function () {
                var data = that.frameworkTable.row( this ).data();
                CF.addRemoveShownFrameworks(data.framework, CONST.add);
                CF.sendRequest(data.framework);
                that.$modalContainer.modal('hide');
            });

            this.$filterField.on('focus', function() {
                $(this).select();
            });
        },

        hideCurrentFrameworks: function(currentFrameworks) {
            var i=0;
            var regexNames = "";
            if(currentFrameworks.length !== 0) {
                for(i=0; i<currentFrameworks.length; i++) {
                    regexNames += currentFrameworks[i] + "|";
                }
                regexNames = regexNames.slice(0, -1);    //remove last "|"

                this.frameworkTable
                    .columns(1) //The index of column to search
                    .search('^(?:(?!(' + regexNames + ')).)*$\r?\n?', true, false) //The RegExp search all string that not cointains values
                    .draw();
            } else {
                this.frameworkTable
                    .search( '' )   // Clear all searches
                    .columns().search( '' )
                    .draw();
            }
        }
    }

    /* Compare framework page functions */
    var CF = {
        
        initVariables: function() {
            this.columnTransform = [4,4,4,3,15,2]; // first 3 are 3 column layout and then 4,5,6 column
            this.currentFrameworks = this.getUrlParams();
            this.frameworkOrder = this.currentFrameworks.concat("","","","","","");
        },

        cacheElements: function() {
            this.$frameworkTable = $('#addFrameworksTable');
            this.$frameworkHeaderContainer = $('#frameworkheader-container');
            this.$frameworkDevSpecContainer = $('#framework-dev-spec-container');
            this.$frameworkHardwareFeatContainer = $('#framework-hardware-feature-container');
            this.$frameworkSupportFeatContainer = $('#framework-support-feature-container');
            this.$frameworkResourcesContainer = $('#framework-resources-container');
            //Sub containers from tool specification
            this.$toolTecCon = $('#toolTecCon');
            this.$toolAnnCon = $('#toolAnnCon');
            this.$toolVerCon = $('#toolVerCon');
            this.$toolPlaCon = $('#toolPlaCon');
            this.$toolLanCon = $('#toolLanCon');
            this.$toolProCon = $('#toolProCon');
            this.$toolLicCon = $('#toolLicCon');
            this.$toolSrcCon = $('#toolSrcCon');
            this.$toolCostCon = $('#toolCostCon');

            this.$addFrameworkButton = $('.add-framework');
            this.$msg = $('#msg');
            this.$collapseButton = $('#btnCollapseAll');
        },

        init: function() {
            this.initVariables();
            this.cacheElements();
            this.bindEvents();
            this.initTooltip();

            this.loadComparisonData();
            this.nothingLeft();
            this.figOutAddButton();

            DataTable.init(this.$frameworkTable);

            console.log( "all init and Bindings complete!" );
        },

        bindEvents: function() {
            this.$collapseButton.on('click', function() {
                var panels = $(this).siblings('.panel-group');
                var btnLabel = $(this).children('.btn-label');
                var option = ""
                if($(btnLabel).text() === "Collapse All") {
                    $(btnLabel).text("Open All");
                    option = "hide";
                } else {
                    $(btnLabel).text("Collapse All");
                    option = "show";
                }
                $(panels).each(function() {
                    $(this).find('.collapse').collapse(option);
                });
            });
        },
        // Mandatory Javascript init of bootstrap tooltip component
        initTooltip: function() {
            $('[data-toggle="tooltip"]').tooltip();
        },

        loadComparisonData: function() {
            var i = 0;
            for(i=0; i<this.currentFrameworks.length; i++) {
                this.sendRequest(this.currentFrameworks[i]);
            }
        },
        /*
         * 0 for add and 1 for removal
         * !NOTE: frameworkOrder is needed to ensure that the background
         * color is always unique. We store the position of the framework
         * in the comparison table. 
         */
        addRemoveShownFrameworks: function(frameworkName, addRemove) {
            var compareIndex = 0;
            if(addRemove) {
                //remove element from stored frameworks and free spot
                compareIndex = this.currentFrameworks.indexOf(frameworkName);
                this.currentFrameworks.splice(compareIndex, 1);
                compareIndex = this.frameworkOrder.indexOf(frameworkName);
                this.frameworkOrder[compareIndex] = "";
            } else {
                //add element to stored frameworks and find/fill free spot
                this.currentFrameworks.push(frameworkName);
                compareIndex = this.frameworkOrder.indexOf("");
                this.frameworkOrder[compareIndex] = frameworkName
            }
            this.figOutAddButton();
            this.nothingLeft();
            DataTable.hideCurrentFrameworks(this.currentFrameworks);
            this.updateUrlParams();
        },

        sendRequest: function(data) {
            $.ajax({
                method: "GET",
                url: "../php/searchFramework.php?keyword=" + data,
                dataType: "json",
                
                error: this.errorCallback,
                success: this.succesCallback
            });
        },

        errorCallback: function(jqXHR, status, errorThrown) {
            console.log("Something went wrong with request");
        },

        succesCallback: function(data, status, jqXHR) {
            console.log("Successful request");
            CF.addMarkupToPage(data);
            CF.bindEventNewItem();
        },

        recalculateColumns: function() {
            var $columns = $('.col-md-9 > div');
            var columnWidth = columnWidth = 'col-md-' + this.columnTransform[this.currentFrameworks.length-1];
            $columns.each(function(index) {
                $(this).alterClass('col-md-*', columnWidth);
            });
            return columnWidth;
        },

        figOutAddButton: function() {
            if(this.currentFrameworks.length > (CONST.maxNumbComparisons-1)) {
                this.$addFrameworkButton.addClass('disabled');
                this.$addFrameworkButton.prop('disabled', true);
            } else {
                this.$addFrameworkButton.removeClass('disabled');
                this.$addFrameworkButton.removeProp('disabled');
            }
        },

        updateUrlParams: function() {
            // get current url
            var i = 0;
            var newUrl = window.location.href;
            if(newUrl.indexOf('?') === -1) {
                newUrl += '?frameworks='
            } else {
                if(newUrl.indexOf('=') === -1) newUrl += '=';
                newUrl = newUrl.substring(0, (newUrl.indexOf('=') + 1));
            }
            // add currentFrameworks to url
            for(i=0; i<this.currentFrameworks.length; i++) {
                newUrl += this.currentFrameworks[i] + ";"
            }
            // remove last ';' from newUrl
            newUrl = newUrl.slice(0, -1);
            if (history.pushState) {
                window.history.pushState({path:newUrl},'',newUrl);
            }
        },

        addMarkupToPage: function(data) {
            var frameworkPos = this.frameworkOrder.indexOf(data.framework);
            var columnWidth = this.recalculateColumns();
            var frameworkClass = data.framework.replace(/[^a-zA-Z0-9]/g, "")

            var contents = '<div class="' + columnWidth + ' header-container head' + (frameworkPos+1) + '">' + data.header +	'</div>';
            this.$frameworkHeaderContainer.append(contents);
            // Add tool specification markup
            contents = '<div class="' + columnWidth + ' no-padding centered body' + (frameworkPos+1) + ' ' + frameworkClass + ' flex-item">' + data.toolTecCon + '</div>';
            this.$toolTecCon.append(contents);
            contents = '<div class="' + columnWidth + ' no-padding centered body' + (frameworkPos+1) + ' ' + frameworkClass + ' flex-item">' + data.toolAnnCon + '</div>';
            this.$toolAnnCon.append(contents);
            contents = '<div class="' + columnWidth + ' no-padding centered body' + (frameworkPos+1) + ' ' + frameworkClass + ' flex-item">' + data.toolVerCon + '</div>';
            this.$toolVerCon.append(contents);
            contents = '<div class="' + columnWidth + ' no-padding centered body' + (frameworkPos+1) + ' ' + frameworkClass + ' flex-item">' + data.toolPlaCon + '</div>';
            this.$toolPlaCon.append(contents);
            contents = '<div class="' + columnWidth + ' no-padding centered body' + (frameworkPos+1) + ' ' + frameworkClass + ' flex-item">' + data.toolLanCon + '</div>';
            this.$toolLanCon.append(contents);
            contents = '<div class="' + columnWidth + ' no-padding centered body' + (frameworkPos+1) + ' ' + frameworkClass + ' flex-item">' + data.toolProCon + '</div>';
            this.$toolProCon.append(contents);
            contents = '<div class="' + columnWidth + ' no-padding centered body' + (frameworkPos+1) + ' ' + frameworkClass + ' flex-item">' + data.toolLicCon + '</div>';
            this.$toolLicCon.append(contents);
            contents = '<div class="' + columnWidth + ' no-padding centered body' + (frameworkPos+1) + ' ' + frameworkClass + ' flex-item">' + data.toolSrcCon + '</div>';
            this.$toolSrcCon.append(contents);
            contents = '<div class="' + columnWidth + ' no-padding centered body' + (frameworkPos+1) + ' ' + frameworkClass + ' flex-item">' + data.toolCostCon + '</div>';
            this.$toolCostCon.append(contents);
            // -----------------------------
            contents = '<div class="' + columnWidth + ' no-padding centered body' + (frameworkPos+1) + ' ' + frameworkClass + '">' + data.dev_specification + '</div>';
            this.$frameworkDevSpecContainer.append(contents);
            contents = '<div class="' + columnWidth + ' no-padding centered body' + (frameworkPos+1) + ' ' + frameworkClass + '">' + data.hardware_features + '</div>';
            this.$frameworkHardwareFeatContainer.append(contents);
            contents = '<div class="' + columnWidth + ' no-padding centered body' + (frameworkPos+1) + ' ' + frameworkClass + '">' + data.support_features + '</div>';
            this.$frameworkSupportFeatContainer.append(contents);
            contents = '<div class="' + columnWidth + ' no-padding centered body' + (frameworkPos+1) + ' ' + frameworkClass + '">' + data.resources + '</div>';
            this.$frameworkResourcesContainer.append(contents);
        },

        bindEventNewItem: function() {
            var that = this;
            // First remove all click handlers and then re-attach to include new ones
            $('.glyphicon-remove-circle').off('click')
            $('.glyphicon-remove-circle').on('click', function() {
                var parentHeaderContainer = $(this).parents('.header-container');
                var frameworkName = $(parentHeaderContainer).find('h4').text();
                var frameworkClass = frameworkName.replace(/[^a-zA-Z0-9]/g, "")
                var $parentBodyContainers = $('.' + frameworkClass);
                that.addRemoveShownFrameworks(frameworkName, CONST.remove);
                
                $(parentHeaderContainer).remove();
                $parentBodyContainers.remove();

                that.recalculateColumns();
            });
        },

        getUrlParams: function () {
            var i = 0
            var vars = [], hash = [];
            var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
            for(i = 0; i < hashes.length; i++) {
                hash = hashes[i].split('=');
                if(hash[0] === "frameworks" && hash.length > 1) {
                    vars = hash[1].split(';');
                }
            }
            //replace %20 with " "
            for(i=0; i < vars.length; i++) {
                vars[i] = vars[i].replace(/%20/g, " ");
            }
            return vars;
        },

        hidePanels: function() {
            $('.compare-body').hide();
        },

        showPanels: function() {
            $('.compare-body').show();
        },
        // Check if there are frameworks being compared (if not show a message)
        nothingLeft: function() {
            if (this.currentFrameworks.length === 0) {
                this.hidePanels();
                this.$msg.show();
            } else {
                this.showPanels();
                this.$msg.hide();
            }
        }

    }


    $( document ).ready(function() {
        console.log( "Document ready!" );
        CF.init();
    });

    window.addEventListener("popstate", function(e) {
        window.location.reload();
    });

    /* 
     * HELPER Function for wildcard class removal with jQuery 
     *
     * https://gist.github.com/peteboere/1517285
     * LICENSE: MIT-license 
     */
    $.fn.alterClass = function ( removals, additions ) {  
        var self = this;
        if ( removals.indexOf( '*' ) === -1 ) {
            // Use native jQuery methods if there is no wildcard matching
            self.removeClass( removals );
            return !additions ? self : self.addClass( additions );
        }
        var patt = new RegExp( '\\s' + 
                removals.
                    replace( /\*/g, '[A-Za-z0-9-_]+' ).
                    split( ' ' ).
                    join( '\\s|\\s' ) + 
                '\\s', 'g' );
        self.each( function ( i, it ) {
            var cn = ' ' + it.className + ' ';
            while ( patt.test( cn ) ) {
                cn = cn.replace( patt, ' ' );
            }
            it.className = $.trim( cn );
        });
        return !additions ? self : self.addClass( additions );
    };

})(jQuery, window, document);

