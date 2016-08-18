;(function($, window, document, undefined) {
    'use strict';

    $(document).ready(function() {
        $('#example').DataTable( {
            stateSave: true,
            "info": false,
            "paging": false,
            "ajax": "data/data.txt",
            "columns": [
                { "data": "name" },
                { "data": "position" },
                { "data": "office" },
                { "data": "extn" },
                { "data": "start_date" },
                { "data": "salary" }
            ]
        });
    });


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

    setWebsiteType: function() {

      var viewport_width = this.$window.width();

      if(viewport_width > 700) {
        this.websiteType = 'large';
      } else {
        this.websiteType = 'small';
      }
    },
    GetWizardValues: function() {

      // Werte in Array speichern
      var wizzard_values = [];

      $(":checked").each(function(index){
        wizzard_values.push($(this).attr("name"));
      });

      // inaktive Labels ausblenden
      // $("input:not(:checked)").parent("label").addClass("unchecked");
      return wizzard_values;

    },
    validateFrameworks: function(wizard_values) {

      $('.selected').removeClass('selected');
      this.count = 0;

      if(wizard_values.length === 0) {

        this.$framework.slideDown();
        this.$reset.slideUp();

      } else {
        this.$reset.slideDown();

        this.$framework.each(function() {

          var
          show = 0,
          that = $(this);

          $.each(wizard_values, function(key, value) {

            var feature = that.find('.' + value);

            if(feature.length) {
              MFCC.count++;
              show++;
              feature.addClass('selected');
            }

          });

          // ein und ausblenden der frameworks
          if(show === wizard_values.length) {
            that.slideDown();
          } else {
            that.slideUp();
          }

        });
      }

      // einzelnen Eintrag einblenden
      // console.log(MFCC.count);
      // if(this.count === 1) {
      //   $('.framework:visible').find('.accordion-header').trigger('click');
      // }
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

  MFCC.init();
*/

    var filterForm = {
        
        initVariables: function() {
            this.filterField = $("input#filter");
            this.frameworks = $(".framework");
            console.log("variables initialized");
        },

        init: function() {
            this.initVariables();
            this.bindEvents();
            console.log("filter init complete");
        },

        bindEvents: function() {
            this.filterField.on('input', function() {
                filterForm.filterFrameworks($(this).val());
            });

            this.filterField.on('focus', function() {
                $(this).select();
                //filterForm.clearFilterField();
                //filterForm.resetFrameworks();
            })

        },

        filterFrameworks: function(filterText) {
            this.frameworks.each( function() {
                var framework = (($(this).find(".framework-title"))[0].innerHTML).toLowerCase();    // get text from div
                var textCompare = framework.indexOf(filterText.toLowerCase());
                
                if( textCompare === -1 ) {
                    $(this).slideUp();
                } else {
                    $(this).slideDown();
                }
            });
        },

        clearFilterField: function() {
            this.filterField.val("");
        },

        resetFrameworks: function() {
            this.frameworks.slideDown();
        }
    }

    var MFCT = {
        

        init: function() {
            filterForm.init();
            console.log("test");
        }
    }

    $( document ).ready(function() {
        console.log( "ready!" );
        MFCT.init();
    });

})(jQuery, window, document);

