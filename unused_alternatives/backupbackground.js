

var response_global = "cats are cool too"

window.addEventListener('DOMContentLoaded', (event) => {
	window.alert("cool beans");
    document.getElementById("mytext").innerHTML = response_global;

});


/*

function myAction(input) { 
    console.log("input value is : " + input.value);

        newish = input.value

        var xxhttp = new XMLHttpRequest();
        xxhttp.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                console.log(this.responseText + "helpme");
            }
        };
        xxhttp.open("POST", "http://127.0.0.1:5000/get_data");
        xxhttp.send(newish);
        //get_data should close once something is sent

//This finally works, just don't touch anything here. Seriously, don't. Trust me. Sincerely: me at 4:00am
// JK gotta change it so we actually do stuff with it. Sincerely: me at 3:18pm
}

*/



function documentEvents() {    
  document.getElementById('ok_btn').addEventListener('click', 
    function() { myAction(document.getElementById('name_textbox'));
  });

  window.alert(input.value);

  // you can add listeners for other objects ( like other buttons ) here 
}



function makePostRequest(path) {
    return new Promise(function (resolve, reject) {
        axios.post(path).then(
            (response) => {
                var result = response.data;
                console.log('Processing Request');
                resolve(result);
            },
                (error) => {
                reject(error);
            }
        );
    });
}





chrome.tabs.onActivated.addListener(function (activeInfo) {
    chrome.tabs.get(activeInfo.tabId, function (tab) {
        y = tab.url;
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                console.log(this.responseText);
            }
        };
        xhttp.open("POST", "http://127.0.0.1:5000/send_url");
        xhttp.open("POST", "http://127.0.0.1:5000/read_page");
        xhttp.send("url=" + y);

        //window.alert(this.response)

    });
});

// send HTTP request above

// the actual listener below for when switching tabs. Activated whenever tabs are updated




async function main() {

	const readHTML = () => new Promise(resolve => window.addEventListener('DOMContentLoaded', resolve, { once: true }));

    var x = await readHTML(); //does it even need to be a variable? eh whatever

    var url = "fetching url";

    chrome.tabs.query({currentWindow: true, active: true}, function(tabs){
      url = tabs[0].url

      var xhttp = new XMLHttpRequest();

      //xhttp.open("POST", "http://127.0.0.1:5000/send_url");
      xhttp.open("POST", "http://127.0.0.1:5000/read_page");
      xhttp.send("url=" + tabs[0].url + "s.p.l.i.t.t.e.r.4.5.1.9" + "8");


      xhttp.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
            	response_global = this.responseText;
            	//window.alert(response_global);

            	document.getElementById("mytext").innerHTML = response_global;   

            }
       };



    }); //end of checking the chrome tab

    const readInp = () => new Promise(resolve => document.getElementById('ok_btn').addEventListener('click', resolve, { once: true }));


    var y = await readInp(); 

    var number_of_sents = document.getElementById('name_textbox');

    if (isNaN(number_of_sents.value) === false)
      chrome.tabs.query({currentWindow: true, active: true}, function(tabs){
      url = tabs[0].url


      var xyhttp = new XMLHttpRequest();

      xyhttp.open("POST", "http://127.0.0.1:5000/read_page");
      xyhttp.send("url=" + tabs[0].url + "s.p.l.i.t.t.e.r.4.5.1.9" + number_of_sents.value);



      xyhttp.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
            	response_global = this.responseText;
            	//window.alert(response_global);

            	document.getElementById("mytext").innerHTML = response_global;   

            }
       };



      });
        else
           window.alert("please input a number");




   /*
    document.getElementById('ok_btn').addEventListener('click', function() { 
    	var input = document.getElementById('name_textbox');
    	window.alert(input.value);
    	if (data === parseInt(data, 10))
           alert("data is integer")
        else
           alert("data is not an integer")

  });

  */


} //end of main

main();









// define a mapping between tabId and url: this might be REMOVED LATER. detects when tab is closed, dont rlly need that
// unless this is whats stopping it from logging every tab. Then edit this somehow? tbd
var tabToUrl = {};

chrome.tabs.onUpdated.addListener(function (tabId, changeInfo, tab) {
    //store tabId and tab url as key value pair:
    tabToUrl[tabId] = tab.url;
});

chrome.tabs.onRemoved.addListener(function (tabId, removeInfo) {
    //since tab is not available inside onRemoved,
    //we have to use the mapping we created above to get the removed tab url:
    console.log(tabToUrl[tabId]);

    var xhttp2 = new XMLHttpRequest();
    xhttp2.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            console.log(this.responseText);
        }
    };
    xhttp2.open("POST", "http://127.0.0.1:5000/quit_url");
    xhttp2.send("url=" + tabToUrl[tabId]);

    // Remove information for non-existent tab
    delete tabToUrl[tabId];

});


