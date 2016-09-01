;(function($, window, document, undefined) {
    'use strict';

    /* Add framework to comparison searchbox */
    var SearchModal = {

        initVariables: function() {
            this.ajaxTimer = null;
            this.ajaxBusy = false;
            this.currentParams = "";
            this.$searchfield = $("#search-field-modal");
            this.$modalContainer = $("#addFrameworkModal");
        },

        init: function() {
            this.initVariables();
            this.bindEvents();
            console.log( "init and Bindings searchModal complete!" );
        },

        bindEvents: function() {
            var that = this;
            this.$modalContainer.on('shown.bs.modal', function (){
                // On modal overlay shown focus the search field
                that.focusInput();
                that.getDefaultFrameworks();
            });
        },

        getDefaultFrameworks: function() {
            this.executeSearch("Smartface");
        },

        executeSearch: function(value) {
            this.ajaxTimer = setTimeout(this.sendAjaxRequest.bind(this, value), 200)
        },

        sendAjaxRequest: function(value) {
            if (this.ajaxBusy) {
                //cancel it if necessary
                return;
            }
            this.ajaxBusy = true;
            this.startRequestCallback();
            this.currentParams = CF.getCurrentComparedFrameworks();
            $.ajax({
                url: CF.ajaxURL + 'keyword=' + encodeURIComponent(value) + this.currentParams,
                type: 'GET',
                dataType: 'json',
                error: this.errorRequestCallback(),
                success: this.successRequestCallback()
            });

        },

        startRequestCallback: function() {
            // Show loading indicator
        },

        successRequestCallback: function(result, status) {
            // Request was successful
            console.log("Success!");
            this.ajaxBusy = false;
            this.displayResults(result, status);
        },

        errorRequestCallback: function(jqXHR, textStatus, errorThrown) {
            // Show error message
            console.log("Error occcured during ajax request: " + errorThrown)
        },

        displayResults: function(result, status) {
            var resultHTML = "";

        },

        focusInput: function() {
            this.$searchfield.focus();
        }
    }


    /* Compare framework page functions */
    var CF = {
        
        initVariables: function() {
            this.ajaxURL = "http://localhost/crossmos_projects/decisionTree/php/searchFramework.php?";
            this.beingCompared = [];
            
        },

        init: function() {
            this.initVariables();
            this.bindEvents();

            SearchModal.init();

            console.log( "all init and Bindings complete!" );
        },

        bindEvents: function() {
            
        },

        getCurrentComparedFrameworks: function() {
            if(this.beingCompared.length > 0) return "&currentFrameworks=" + this.beingCompared.join(';');
            else return ""; 
        }
    }


    $( document ).ready(function() {
        console.log( "Document ready!" );
        CF.init();
    });

})(jQuery, window, document);

