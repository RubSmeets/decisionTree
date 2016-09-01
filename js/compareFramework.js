;(function($, window, document, undefined) {
    'use strict';

    /* Add framework to comparison searchbox */
    var SearchModal = {

        initVariables: function() {
            this.$modalContainer = $("#addFrameworkModal");
        },

        init: function() {
            this.initVariables();
            this.bindEvents();
            console.log( "init and Bindings searchModal complete!" );
        },

        bindEvents: function() {
            
        },



    }

    /* Datatable functionality */
    var DataTable = {
        initVariables: function() {
            this.$modalContainer = $("#addFrameworkModal");
            this.$frameworkTable = $("#addFrameworksTable");
            this.$filterFieldContainer = $('#addFrameworksTable_filter');
            this.$filterField = $('#addFrameworksTable_filter').find(':input');
        },

        init: function($frameworkTable) {
            this.initTable($frameworkTable);
            this.initVariables();
            this.cleanMarkup();
            this.bindEvents();
        },

        initTable: function($frameworkTable) {
            $frameworkTable.DataTable({
                ajax: {
                    url: '../php/testThumbFrameworks.php',
                    dataSrc: "frameworks"
                },
                columns: [
                    {data: 'thumb_img',
                        render: function (data, type, row) {
                            if (type ==='display') {
                                var thumbs = "";
                                thumbs = '<img src="'+data+'" class="compareThumb"/>';
                                return thumbs;
                            } else return '';
                        }
                    },
                    {data: 'framework',
                        render: function (data, type, row) {
                            if (type ==='display') {
                                var title = "";
                                title = '<img src="'+data+'" class="compareThumb"/>';
                                return title;
                            } else return '';
                        }
                    }
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
        }


    }

    /* Compare framework page functions */
    var CF = {
        
        initVariables: function() {
            this.$frameworkTable = $('#addFrameworksTable');
        },

        init: function() {
            this.initVariables();
            this.bindEvents();

            DataTable.init(this.$frameworkTable);
            SearchModal.init();

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

