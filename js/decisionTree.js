/*
 * Resources:
 * - http://www.sitecrafting.com/blog/jquery-caching-convention/ (best practice jquery naming convention)
 * - 
 */
(function($, window, document, undefined) {
    'use strict';

    var CONST = {
        maxCompared: 5,
        minCompared: 2,
        compareLabelText: "Compare"
    }

    /* Filter-textbox element functions */
    var filterForm = {
        
        initVariables: function() {
            this.filterText = "";
            this.domCache = {};
        },

        cacheElements: function() {
            this.domCache.filterField = $("input#filter");
        },

        init: function() {
            this.initVariables();
            this.cacheElements();
            this.bindEvents();
        },

        bindEvents: function() {
            var that = this;
            this.domCache.filterField.on('input', function() {
                that.filterText = $(this).val();
                main.filterFrameworks();
            });

            this.domCache.filterField.on('focus', function() {
                $(this).select();
            });

        },

        CheckFrameworkName: function(filterText, framework) {
            var frameworkName;
            var textCompare;
            this.filterText = filterText;

            frameworkName = (($(framework).find(".thumb-caption"))[0].innerHTML).toLowerCase();    // get text from div
            textCompare = frameworkName.indexOf(filterText.toLowerCase());
            
            if( textCompare === -1 ) return false;
            else return true;
        },
        // Not used (maybe in future)
        clearFilterField: function() {
            this.domCache.filterField.val("");
        }
    }
    /* Mobile framework comparison tool functionality */
    var main = {
        initVariables: function() {
            this.filterTerms = [];
            this.comparedItems = [];
            this.domCache = {};
        },

        cacheElements: function() {
            this.domCache.checkboxes = $('[type=checkbox]');
            this.domCache.frameworks = $(".framework");
            this.domCache.filterContainer = $('.filters');
            this.domCache.msg = $("#msg");
            this.domCache.msgInfoCompare = $("#msgInfoCompare");
            this.domCache.clearButton = $('.btn-clear');
            this.domCache.compareCheckboxes = $('[type=checkbox].compare-checkbox');
        },

        init: function() {
            this.initVariables();
            this.cacheElements();
            this.bindEvents();

            filterForm.init();
            this.initTooltip();
            this.resetPage();
            frameworkPopularity.init();
        },
        // Mandatory Javascript init of bootstrap tooltip component
        initTooltip: function() {
            $('[data-toggle="tooltip"]').tooltip();
        },

        bindEvents: function() {
            var that = this;
            this.domCache.checkboxes.on('input change', function() {
                that.toggleClearButton();
            });

            this.domCache.compareCheckboxes.on('input change', function() {
                that.updateCompareUrl(this);
                that.determineCompareVisibility();
            });

            this.domCache.filterContainer.on('input change', function() {
                that.getCheckedFilterTerms();
                that.filterFrameworks();
            });

            this.domCache.clearButton.on('click', function() {
                that.domCache.checkboxes.each( function() {
                  if( $(this).is(':checked') ) {
                      $(this).prop("checked", false).change();  // Force change event
                  }
                });
                that.collapseAll();
            });
            // hide bootstrap Alert
            $("[data-hide]").on("click", function(){
                $(this).closest("." + $(this).attr("data-hide")).hide();
            });
        },

        getCheckedFilterTerms: function() {
            this.filterTerms = [];
            var that = this;

            this.domCache.checkboxes.each( function() {
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

            if (filterTerms.length === foundFeatures) return true;
            else return false;
        },
        // Do a combined filter of checkboxes and form search
        filterFrameworks: function() {
            var that = this;
            // Clear selected class
            $('.selected').removeClass('selected');

            this.domCache.frameworks.each( function() {
                if( that.CheckFrameworkFeature(that.filterTerms, this) && filterForm.CheckFrameworkName(filterForm.filterText, this) ) {
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
            var $frameworkLabel = $(compareCheckbox).siblings('.thumb-caption');
            var frameworkName = $($frameworkLabel[0]).text();
            var $compareButtons = $('.compare-link');
            var $mainCompareBtn = $('#goToCompareBtn');
            var href = "html/compare.html?frameworks=";
            var compareIndex = 0;
            var i = 0;

            if($(compareCheckbox).is(':checked')) {
                if(this.comparedItems.length === (CONST.maxCompared)) {
                    this.domCache.msgInfoCompare.show();
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
            $compareButtons.prop('href', href);
            $mainCompareBtn.prop('href', href);
        },
        
        determineCompareVisibility: function() {
            var $compareButtons = $('.compare-link');
            var $checkboxCompareLabels = $(".compare-label");
            var $compareCheckbox = null;
            var $checkboxLabel = null;

            if(this.comparedItems.length > (CONST.maxCompared)) return; // do nothing

            if(this.comparedItems.length > (CONST.minCompared-1)) {
                $compareButtons.each(function () {
                    $compareCheckbox = $(this).siblings(':input');
                    $checkboxLabel = $(this).siblings('label');
                    if($compareCheckbox.is(":checked")) {
                        $checkboxLabel.text("");
                        $(this).removeClass("hidden");
                    } else {
                        $(this).addClass("hidden");
                        $checkboxLabel.text(CONST.compareLabelText);
                    }
                });
                return; // go Back
            }
            // every other situation hide button
            $compareButtons.addClass("hidden");
            $checkboxCompareLabels.text(CONST.compareLabelText);  // Could be done better...
        },

        // Enable and disable button
        toggleClearButton: function() {
            if( this.domCache.checkboxes.is(":checked") ) {
              this.domCache.clearButton.prop('disabled', false);
            } else {
              this.domCache.clearButton.prop('disabled', true);
            }
        },
        // Check if there are frameworks left (if not show a message)
        nothingLeft: function() {
            if ($('.framework.hid').length === this.domCache.frameworks.length) {
                this.domCache.msg.show();
            } else {
                this.domCache.msg.hide();
            }
        },
        // collapse all detail panels
        collapseAll: function() {
            var $panels = $('.caption');
            $panels.each(function() {
                $(this).find('.collapse').collapse("hide");
            });
        },
        // Back to normal state
        resetFrameworks: function() {
            this.domCache.frameworks.slideDown();
            this.domCache.frameworks.removeClass("hid");
        },
        // Reset markup of page
        resetPage: function() {
            this.domCache.checkboxes.prop("checked", false);
        }
    }

    var frameworkPopularity = {
        initVariables: function() {
            
        },

        cacheElements: function() {

        },
        
        init: function() {
            this.initVariables();
            this.cacheElements();
            this.loadTwitterData();
        },

        loadTwitterData: function() {
            var $twitterDiv = $(".fa-twitter");
            var that = this;
            $twitterDiv.each(function () {
                var twitterName = $(this).prop("id");
                // API not supported by twitter - http://stackoverflow.com/questions/17409227/follower-count-number-in-twitter
                $.ajax({
                    url: "https://cdn.syndication.twimg.com/widgets/followbutton/info.json?screen_names=" + twitterName,
                    dataType : 'jsonp',
                    crossDomain : true,
                    success: that.twitterSuccessCallBack,
                    error: that.twitterErrorCallBack
                })
            });
        },

        twitterErrorCallBack: function() {
            console.log("Failed to make request");
        },

        twitterSuccessCallBack: function(data, status, jqXHR) {
            var $twitterLabel = $("#" + data[0].screen_name.toLowerCase()).siblings("span")[0];
            $($twitterLabel).text((data[0].formatted_followers_count).slice(0, -10));
            console.log("success to make request");
        }

    }

    $( document ).ready(function() {
        main.init();
    });

})(jQuery, window, document);


