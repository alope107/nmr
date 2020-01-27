/*

CHANGE ME BACK


*/
//var POST_URL = "https://us-central1-cloud-functions-246501.cloudfunctions.net/TestFunc";
var POST_URL = "https://httpbin.org/post";
//var POST_URL = "https://mqzfybr9e6.execute-api.us-west-2.amazonaws.com/default/maliceFormSubmit";
var API_KEY = "DUMMY";

function onOpen(e) {
  FormApp.getUi()
      .createAddonMenu()
      .addItem('BWAH', 'showSidebar')
      .addItem('ADJUST', 'adjustFormSubmitTrigger')
      .addToUi();
  
  Logger.log("Hey now you're a rock star get your game on go play")
}

function stuff() {
  var form = FormApp.getActiveForm();
  var responses = form.getResponses();
  var latestResponse = responses[responses.length - 1];
  var itemResponses = latestResponse.getItemResponses();
  for(var i = 0; i < itemResponses.length; i++) {
    var item = itemResponses[i].getItem();
    if (item.getTitle() === "Filez") {
      var f = itemResponses[i].getResponse();
      //sendFile(itemResponses[i].getResponse());
      Logger.log("ba dum dum dum")
      Logger.log(f);
      //console.log(itemResponses[i].getResponse());
    }
    var answer = itemResponses[i].getResponse();
    Logger.log(item.getTitle());
    Logger.log(answer);
  }
}

function sendFile(f) {
  Logger.log("Sending file");
  
  var formData = {
  'file': f
  };
  
  var options = {
        "method": "post",
        "payload": formData
  };

  rez  = UrlFetchApp.fetch(POST_URL, options);
  Logger.log("HEY");
  Logger.log(rez);
}

function onInstall(e) {
  onOpen(e);
}

/**
 * Adjust the onFormSubmit trigger based on user's requests.
 */
function adjustFormSubmitTrigger() {
  Logger.log("adjForm")
  var form = FormApp.getActiveForm();
  var triggers = ScriptApp.getUserTriggers(form);
  var settings = PropertiesService.getDocumentProperties();

  // Create a new trigger if required; delete existing trigger
  //   if it is not needed.
  for (var i = 0; i < triggers.length; i++) {
    if (triggers[i].getEventType() == ScriptApp.EventType.ON_FORM_SUBMIT) {
      Logger.log("DELETE THAT TRIGGER");
      ScriptApp.deleteTrigger(triggers[i]);
    }
  }
  var trigger = ScriptApp.newTrigger('respondToFormSubmit')
  .forForm(form)
  .onFormSubmit()
  .create();
}

function respondToFormSubmit(e) {
  /*console.log("Do you see what I see????");
  Logger.log("Respond to form submittal!");
  console.log(JSON.stringify(e));
  var headers = {
    "x-api-key": API_Key,
  };
  
  var options = {
        "method": "post",
    "headers": headers,
        'contentType': 'application/json',
        "payload": JSON.stringify({
            "message": "SUCK IT"
        })
    };

   UrlFetchApp.fetch(POST_URL, options);*/
}
function onSubmit(e) {
  Logger.log("Submitted!")
}