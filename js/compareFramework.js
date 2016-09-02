;(function($, window, document, undefined) {
    'use strict';

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
                
            } );
        }


    }

    /* Compare framework page functions */
    var CF = {
        
        initVariables: function() {
            
        },

        cacheElements: function() {
            this.$frameworkTable = $('#addFrameworksTable');
        },

        init: function() {
            this.initVariables();
            this.cacheElements();
            this.bindEvents();

            DataTable.init(this.$frameworkTable);

            console.log( "all init and Bindings complete!" );
        },

        bindEvents: function() {
            
        },
    }


    $( document ).ready(function() {
        console.log( "Document ready!" );
        CF.init();
    });

})(jQuery, window, document);

