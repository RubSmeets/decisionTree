;(function($, window, document, undefined) {
    'use strict';

    var CONST = {
        maxCompared: 5,
        minCompared: 2
    }

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

            frameworkName = (($(framework).find(".thumb-caption"))[0].innerHTML).toLowerCase();    // get text from div
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
            this.comparedItems = [];
            this.checkboxes = $('[type=checkbox]');
            this.frameworks = $(".framework");
            this.filterContainer = $('.filters');
            this.msg = $("#msg");
            this.msgInfoCompare = $("#msgInfoCompare");
            this.clearButton = $('.btn-clear');
            this.$compareCheckboxes = $('[type=checkbox].compare-checkbox');
            console.log("variables initialized");
        },

        init: function() {
            this.initVariables();
            this.bindEvents();

            filterForm.init();
            this.initTooltip();
            this.resetPage();
            console.log("init framework comparison complete");
        },
        // Mandatory Javascript init of bootstrap tooltip component
        initTooltip: function() {
            $('[data-toggle="tooltip"]').tooltip();
        },

        bindEvents: function() {
            var that = this;
            this.checkboxes.on('input change', function() {
                MFCT.toggleClearButton();
                console.log("fired input change global");
            });

            this.$compareCheckboxes.on('input change', function() {
                that.updateCompareUrl(this);
                that.determineCompareVisibility();
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
                MFCT.collapseAll();
            });

            $("[data-hide]").on("click", function(){
                $(this).closest("." + $(this).attr("data-hide")).hide();
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

        // update compare url
        updateCompareUrl: function(compareCheckbox) {
            var frameworkLabel = $(compareCheckbox).siblings('.thumb-caption');
            var frameworkName = $(frameworkLabel[0]).text();
            var compareButtons = $('.compare-link');
            var $mainCompareBtn = $('#goToCompareBtn');
            var href = "html/compare.html?frameworks=";
            var compareIndex = 0;
            var i = 0;

            if($(compareCheckbox).is(':checked')) {
                if(this.comparedItems.length === (CONST.maxCompared)) {
                    this.msgInfoCompare.show();
                    $(compareCheckbox).prop('checked', false);  // clear checkboxe
                    return; // do not update url or push framework
                }
                this.comparedItems.push(frameworkName);
            } else {
                //remove element
                compareIndex = this.comparedItems.indexOf(frameworkName);
                this.comparedItems.splice(compareIndex, 1);
            }

            // Update href value of link button
            for(i=0; i<this.comparedItems.length; i++) {
                href += this.comparedItems[i] + ";"
            }
            // remove last ';' from href
            href = href.slice(0, -1);
            $(compareButtons).prop('href', href);
            $mainCompareBtn.prop('href', href);
        },
        
        determineCompareVisibility: function() {
            var compareButtons = $('.compare-link');
            var compareCheckbox = null;

            if(this.comparedItems.length > (CONST.maxCompared)) return; // do nothing

            if(this.comparedItems.length > (CONST.minCompared-1)) {
                compareButtons.each(function () {
                    compareCheckbox = $(this).siblings(':input');
                    if($(compareCheckbox).is(":checked")) {
                        $(this).removeClass("hidden");
                    } else {
                        $(this).addClass("hidden");
                    }
                });
                return; // go Back
            }
            // every other situation hide button
            compareButtons.addClass("hidden");
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
        // collapse all detail panels
        collapseAll: function() {
            var panels = $('.caption');
            $(panels).each(function() {
                $(this).find('.collapse').collapse("hide");
            });
        },
        // Back to normal state
        resetFrameworks: function() {
            this.frameworks.slideDown();
            this.frameworks.removeClass("hid");
        },
        // Reset markup of page
        resetPage: function() {
            this.checkboxes.prop("checked", false);
        }
    }

    $( document ).ready(function() {
        console.log( "ready!" );
        MFCT.init();
    });

})(jQuery, window, document);

