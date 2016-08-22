;(function($, window, document, undefined) {
    'use strict';

  /************************************************************
    @description Filter
    todo: performance, caching
  *************************************************************/
/*  var Filter = {
    cacheElements: function() {
      this.$filter_form = $('.filter-form').find('form');
      this.$filter = $('.filter');
      this.$msg = $('.msg').hide();
    },
    init: function() {
      this.cacheElements();
      this.bindEvents();
    },
    bindEvents: function() {

      // Avoid page load upon submit
      this.$filter_form.on('submit', function(event) {
        event.preventDefault();
      });

      this.$filter_form.find('input').on('focus', function() {
        Filter.resetFilter();
      });

      // Liste filtern
      this.$filter_form.find('input').on('input keyup', function() {

        if ($(this).val().length > 2) {
          Filter.filterItems($(this).val());
        } else {
          $('.framework').slideDown();
        }

        // check if something was found
        Filter.nothingLeft();
      });
    },
    filterItems: function(input_value) {

      $('.framework:visible').each(function() {

        var test = $(this).find('.accordion-header').text().toLowerCase().indexOf(input_value.toLowerCase());

        if (test === -1) {
          $(this).slideUp();
        } else {
          $(this).slideDown();
        }

      });
    },
    nothingLeft: function() {
      if($('.framework:visible').length === 0) {
        this.$msg.show();
      } else {
        this.$msg.hide();
      }
    },
    resetFilter: function() {
      this.$filter.find('input:checked').prop('checked', false).trigger('change');
    },
  };
*/

  /************************************************************
    @description MobileFrameworksComparisonChart
  *************************************************************/
 /* var MFCC = {
    cacheElements: function() {
      this.$document = $(document);
      this.$filter = $('.filter');
      this.$framework = $('.framework');
      this.$getstarted = $('.getstarted');
      this.$legacy = $('.legacy');
      this.$reset = $('.reset').hide();
      this.$window = $(window);

      this.$checkbox = this.$filter.find('.checkbox');
      this.$platform = this.$filter.find('.heading:first-child');
    },
    init: function() {

      this.cacheElements();
      this.setWebsiteType();
      this.bindEvents();
      this.setupLegend();

      Accordion.init();
      Filter.init();
      TrackExternalLinks.init();

    },
    bindEvents: function() {

      this.$filter.on('input change', function() {
        var wizard = MFCC.GetWizardValues();
        MFCC.validateFrameworks(wizard);
      });

      if(this.websiteType === 'large') {
        this.$document.on('accordion-ready', function () {
          // ersten Eintrag öffnen
          MFCC.$platform.trigger('click');
        });
      }

      // Auswahl hervorheben
      this.$checkbox.on('input change', function() {
        $(this).closest('label').toggleClass('checked');
      });

      // reset Button
      this.$reset.on('click', function(event) {
        event.preventDefault();
        Filter.resetFilter();
      });
    },

    validateFrameworks: function(wizard_values) {

      $('.selected').removeClass('selected');
      this.count = 0;

      if(wizard_values.length === 0) {

        this.$framework.slideDown();
        this.$reset.slideUp();

      } else {
        this.$reset.slideDown();



    },
    setupLegend: function () {

      $('.legend li').hide();

      $('.feature').on('mouseover', function() {

        $('.legend').show();

        $(".legend ." + $(this).data('support')).show();
      });

      $('.feature').on('mouseout', function() {
        $('.legend, .legend li').hide();
      });

      $(document).on('mousemove', function(e){
        $(".legend, .help").css('top', e.pageY);
        $(".legend, .help").css('left', e.pageX+5);
      });
    }
  };
*/
    var filterForm = {
        
        initVariables: function() {
            this.filterText = "";
            this.filterField = $("input#filter");
            this.msg = $("#msg");
            console.log("variables initialized");
        },

        init: function() {
            this.initVariables();
            this.bindEvents();
            console.log("filter init complete");
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
                //filterForm.resetFrameworks();
            })

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
        },
        // Back to normal state
        resetFrameworks: function() {
            MFCT.frameworks.slideDown();
            MFCT.frameworks.removeClass("hid");
        },
        // Check if there are frameworks left (if not show a message)
        nothingLeft: function() {
            if ($('.framework.hid').length === MFCT.frameworks.length) {
                this.msg.show();
            } else {
                this.msg.hide();
            }
        }
    }

    var MFCT = {
        initVariables: function() {
            this.filterTerms = [];
            this.checkboxes = $('[type=checkbox]');
            this.frameworks = $(".framework");
            this.filterContainer = $('.filters');
            this.clearButton = $('.btn-clear');
            console.log("initialise variables");
        },

        init: function() {
            this.initVariables();
            this.bindEvents();

            filterForm.init();
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

        filterFrameworks: function(filterTerms) {
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

            filterForm.nothingLeft();
        },

        toggleClearButton: function() {
            if( this.checkboxes.is(":checked") ) {
              this.clearButton.prop('disabled', false);
            } else {
              this.clearButton.prop('disabled', true);
            }
        }
    }

    $( document ).ready(function() {
        console.log( "ready!" );
        MFCT.init();
    });

})(jQuery, window, document);

