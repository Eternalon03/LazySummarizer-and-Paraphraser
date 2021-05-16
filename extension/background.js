

var response_global = ""

window.addEventListener('DOMContentLoaded', (event) => {

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

            	response_global = response_global.split("minutes");

            	summary = response_global[1];


            	summary = summary.replace(/\\\"/g, "\"");  //replaces all the /" with just "

              summary = summary.replace(/\\u2013/g, "-");  //replaces all the /" with just "

            	header = response_global[0] + "minutes";

            	header = header.split("Estimated");

            	header2 = "Estimated" + header[1];

            	header1 = header[0];

            	header1 = header1.replace("\"", "");


            	document.getElementById("mytext").innerHTML = summary;

            	document.getElementById("header1").innerHTML = header1;    

            	document.getElementById("header2").innerHTML = header2;   

            	forpara = summary; // so when it first loads I can send this to the paraphrase function

            }
       };



    }); //end of checking the chrome tab

    document.getElementById('ok_btn').addEventListener('click', 
    function() { myAction(document.getElementById('name_textbox'));
    });


    document.getElementById('keywords_btn').addEventListener('click', 
    function() { 

    if (document.getElementById("actual_keywords").innerHTML == "") {

     var url2 = ""

     chrome.tabs.query({currentWindow: true, active: true}, function(tabs){
      url = tabs[0].url

      var xhttp = new XMLHttpRequest();

      xhttp.open("POST", "http://127.0.0.1:5000/get_data");
      xhttp.send("url=" + tabs[0].url);


      xhttp.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
            	response_global = this.responseText;
            	//window.alert(response_global);

            	response_global = response_global.replace(/%%%/g, "<br></br>");    //html line break <br>
            	response_global = response_global.replace(/\"/g, "");   //   /bob/g globally replaces bob


            	document.getElementById("actual_keywords").innerHTML = response_global;
            	document.getElementById("keywords_btn").innerHTML = "Close";


            	var open_keywords = true;


            }
       };
      }); //end of checking the chrome tab


    } else {
      document.getElementById("actual_keywords").innerHTML = "";
      document.getElementById("keywords_btn").innerHTML = "Key Words";

    }


    });

    document.getElementById('paraphrase_btn').addEventListener('click', 
    function() {

      if (document.getElementById("actual_paraphrase").innerHTML == "") {

    	var xhttp = new XMLHttpRequest();  //can be named anything not just xhttp, but not encountering problems rn

        xhttp.open("POST", "http://127.0.0.1:5000/paraphrase_summary");
        xhttp.send(forpara);

    	xhttp.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
            	new_response = this.responseText;

            	new_response = new_response.replace(/\\\"/g, "\"");  //replaces all the /" with just "

            	new_response = new_response.replace(/``/g, "\"");  //replaces all the /" with just "

            	new_response = new_response.substring(1);

            	new_response = new_response.substring(0, new_response.length - 2);

              new_response = new_response.replace(/,/g, ", ");

              new_response = new_response.replace(/\./g, ". ");  //just putting . replaces literally every character with '. '


            	document.getElementById("actual_paraphrase").innerHTML = new_response;
            	document.getElementById("paraphrase_btn").innerHTML = "Close";


            }
       };

     } else {
     	document.getElementById("actual_paraphrase").innerHTML = "";
     	document.getElementById("paraphrase_btn").innerHTML = "Paraphrase";
     }
 


    });  //end of paraphrase button



});


function myAction(input) { 

    console.log("input value is : " + input.value);

    newish = input.value

    var url = "fetching url";

    if (isNaN(input.value) === false) //check if input is an integer. Yes isNan being false means its an integer

     chrome.tabs.query({currentWindow: true, active: true}, function(tabs){
      url = tabs[0].url

      var xxhttp = new XMLHttpRequest();

      xxhttp.open("POST", "http://127.0.0.1:5000/read_page");
      xxhttp.send("url=" + tabs[0].url + "s.p.l.i.t.t.e.r.4.5.1.9" + input.value);


      xxhttp.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
            	response_global = this.responseText;

            	response_global = response_global.split("minutes");

            	summary = response_global[1];


            	summary = summary.replace(/\\\"/g, "\"");  //replaces all the /" with just "

            	header = response_global[0] + "minutes";

            	header = header.split("Estimated");

            	header2 = "Estimated" + header[1];

            	header1 = header[0];

            	header1 = header1.replace("\"", "");


            	document.getElementById("mytext").innerHTML = summary;

            	document.getElementById("header1").innerHTML = header1;    

            	document.getElementById("header2").innerHTML = header2;     

            }
       };



     }); //end of checking the chrome tab

    else
        window.alert("please input a number");



//This finally works, just don't touch anything here. Seriously, don't. Trust me. Sincerely: me at 4:00am
}