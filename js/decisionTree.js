;(function($, window, document, undefined) {
    'use strict';

    /* Filter-textbox element functions */
    var filterForm = {
        
        initVariables: function() {
            this.filterText = "";
            this.filterField = $("input#filter");
        },

        init: function() {
            this.initVariables();
            this.bindEvents();
        },

        bindEvents: function() {
            var that = this;
            this.filterField.on('input', function() {
                that.filterText = $(this).val();
                MFCT.filterFrameworks();
            });

            this.filterField.on('focus', function() {
                $(this).select();
                //filterForm.clearFilterField();
                //MFCT.resetFrameworks();
            });

        },

        CheckFrameworkName: function(filterText, framework) {
            var frameworkName;
            var textCompare;
            this.filterText = filterText;

            frameworkName = (($(framework).find(".framework-title"))[0].innerHTML).toLowerCase();    // get text from div
            textCompare = frameworkName.indexOf(filterText.toLowerCase());
            
            if( textCompare === -1 ) {
                return false;
            } else {
                return true;
            }
        },

        clearFilterField: function() {
            this.filterField.val("");
        }
    }
    /* Mobile framework comparison tool functionality */
    var MFCT = {
        initVariables: function() {
            this.filterTerms = [];
            this.checkboxes = $('[type=checkbox]');
            this.frameworks = $(".framework");
            this.filterContainer = $('.filters');
            this.msg = $("#msg");
            this.clearButton = $('.btn-clear');
            console.log("variables initialized");
        },

        init: function() {
            this.initVariables();
            this.bindEvents();

            filterForm.init();
            this.initTooltip();
            console.log("init framework comparison complete");
        },
        // Mandatory Javascript init of bootstrap tooltip component
        initTooltip: function() {
            $('[data-toggle="tooltip"]').tooltip();
        },

        bindEvents: function() {
            this.checkboxes.on('input change', function() {
                MFCT.toggleClearButton();
            });

            this.filterContainer.on('input change', function() {
                MFCT.getCheckedFilterTerms();
                MFCT.filterFrameworks();
            });

            this.clearButton.on('click', function() {
                MFCT.checkboxes.each( function() {
                  if( $(this).is(':checked') ) {
                      $(this).prop("checked", false).change();
                  }
                });
            });
        },

        getCheckedFilterTerms: function() {
            this.filterTerms = [];
            var that = this;

            this.checkboxes.each( function() {
                if ( $(this).is(':checked') ) {
                  that.filterTerms.push($(this).val());
                }
            });
        },

        CheckFrameworkFeature: function(filterTerms, framework) {
            var foundFeatures = 0;
            var i = 0;
            var $feature;

            for(i=0; i<filterTerms.length; i++) {
                $feature = $(framework).find('.' + filterTerms[i]);
                if ( $feature.length === 1 ) {
                  foundFeatures++;
                  $feature.addClass('selected');
                }
            }

            if (filterTerms.length === foundFeatures) {
                return true;
            } else {
                return false;
            }
        },
        // Do a combined filter of checkboxes and form
        filterFrameworks: function() {
            var that = this;
            // Clear selected class
            $('.selected').removeClass('selected');

            this.frameworks.each( function() {
                if( MFCT.CheckFrameworkFeature(that.filterTerms, this) && filterForm.CheckFrameworkName(filterForm.filterText, this) ) {
                    $(this).slideDown();
                    $(this).removeClass("hid");
                } else {
                    $(this).slideUp();
                    $(this).addClass("hid");
                }
            });

            this.nothingLeft();
        },
        // Enable and disable button
        toggleClearButton: function() {
            if( this.checkboxes.is(":checked") ) {
              this.clearButton.prop('disabled', false);
            } else {
              this.clearButton.prop('disabled', true);
            }
        },
        // Check if there are frameworks left (if not show a message)
        nothingLeft: function() {
            if ($('.framework.hid').length === this.frameworks.length) {
                this.msg.show();
            } else {
                this.msg.hide();
            }
        },
        
        // Back to normal state
        resetFrameworks: function() {
            this.frameworks.slideDown();
            this.frameworks.removeClass("hid");
        }
    }

    $( document ).ready(function() {
        console.log( "ready!" );
        MFCT.init();
    });

})(jQuery, window, document);

