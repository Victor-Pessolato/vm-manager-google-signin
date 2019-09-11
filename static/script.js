
const requestManager = {
    id_token: null,
    makeRequest(options, callback) {
        options['headers'] = {'x-user-token': this.id_token};
        $.ajax(options).done(function(data) {
            callback(data);
        });
    },
    checkOnRequest(zone, operationID, callback) {
        let handle = setInterval(function() {
            requestManager.makeRequest({url: `/operations/${zone}/${operationID}`}, function(data) {
                if(data.status === "DONE") {
                    clearInterval(handle);
                    callback(data);
                }
            });
        },1000);
    }
};

const modalController = {
    open(caller) {
        this["$_caller"] = $(caller);
        if(this.$_caller.hasClass("disabled") == false) {
            this["action"] = this.$_caller.attr("data-action");
            this["target"] = this.$_caller.attr("data-vm");
            this["zone"] = this.$_caller.attr("data-zone");

            $("#confirm_text").html(`Are you sure you wish to ${this.action} <b>${this.target}</b>?`);
            $("#confirm_actions").html(`
                <button class="btn btn-light btn-sm" data-dismiss="modal">
                    CANCEL
                </button>
                <button class="btn btn-info btn-sm font-weight-bold" onclick="modalController.confirm(this)">
                    ${this.action.toUpperCase()}
                </button>`);

            $("#confirm_modal").modal('show');
        }
    },

    confirm(confirmer) {
        let zone = this.zone;
        let $_caller = this.$_caller;
        this["$_confirmer"] = $(confirmer);
        if (this.$_confirmer.hasClass('disabled') == false) {
            $_caller.addClass("disabled");
            requestManager.makeRequest({
                method: "POST",
                url: `/instances/${this.action}`,
                data: {
                    instance: this.target,
                    zone: zone
                }
            }, function(data) {
                if(data.id) {
                    ui.removeSpinner(confirmer);
                    ui.addSpinner($_caller);
                    $("#confirm_modal").modal('hide');
                    requestManager.checkOnRequest(zone, data.id, app.updateInstance);
                }
            });
        }
        ui.addSpinnerToButton(confirmer);
    }
};

const ui = {
    addSpinner($_target) {
        $_target.html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>`);
    },

    addSpinnerToButton(target) {
        $_target = $(target);
        $_spinner = $_target.children(".spinner-border");
        if ($_spinner.length <= 0) {
            $_target.append(` <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>`);
        } else {
            $_spinner.show();
        }
        $_target.addClass("disabled");
    },

    removeSpinner(target) {
        $_target = $(target);
        $_target.children(".spinner-border").hide();
        $_target.removeClass("disabled");
    }
};

const app = {
    load() {
        // Load user data
        this.getUserData();

        // Load instances data
        this.getInstances();
    },

    getUserData() {
        let options = {url: '/get-user-data'};
        requestManager.makeRequest(options, function(data) {
            $("#nav_user_info").html(data);
        });
    },

    getInstances() {
        $_workspace = $("#main-workspace");
        $_workspace.html(`<div id="workspace-spinner" class="spinner-border spinner-border-lg"></div>`);

        requestManager.makeRequest({url: '/zones'}, function(data) {
            if(data.zone_count > 0) {
                function getInstanceByZone() {
                    let zone = data.zones.pop();
                    if(zone) {
                        requestManager.makeRequest({url: '/instances/' + zone.name}, function(data) {
                            // Display data
                            if(!data.message) {
                                $_workspace.prepend(data);
                            }                            
                            // Continue handling the queue 
                            getInstanceByZone();  
                        });
                    } else {
                        $("#workspace-spinner").fadeOut();
                    }
                }

                getInstanceByZone();

            } else {
                $_workspace.html(`<h2 class="text-center">An error occured when trying to fetch GPC zones</h2>`);
            }
        });
    },
    // Updates UI information after tracking progress of a operation
    updateInstance(data) {
        let x = data.zone.lastIndexOf("/");
        let zone = data.zone.substring(x + 1);
        $(`#${data.targetId}`).load(`/instances/${zone}/${data.targetId}`);
    }
};

// Callback for when the user sign in from the web and when we do the first check.
function onSignIn(googleUser) {
    requestManager.id_token = googleUser.getAuthResponse().id_token;
    app.load();
}

// Sign out function from The Google Signin API
function signOut() {
    let auth2 = gapi.auth2.getAuthInstance();
    requestManager.makeRequest({url: '/sign-out'}, function(data) {
        auth2.signOut().then(function () {
            console.log('User signed out.');
            location.reload();
        });
    });
}

// If user is already logged in the browser we check if it's a valid user and if it is registered in our DB
if (auth2.isSignedIn.get()) {
    onSignIn(googleUser);
}