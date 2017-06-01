//==============================================================================================
// Example script to help you build your own local web remote for VoxCommando.
// Via http get requests, we use VC's API to send commands to VC.
// We can also get information back from VC.
// See http://voxcommando.com/mediawiki/index.php?title=API_Application_Programming_Interface
//==============================================================================================

	window.onload = function(){
		var links = document.getElementsByTagName('a')
		
		for (i=0;i<links.length;i++){
			var myCall = links[i].getAttribute('id')//api url
			var myItem = links[i].getAttribute('name')
			getVCdata(myCall,myItem)
			}		
		}
		
	//Displays feedback message at the top of the page
	function UIfeedback(msg){
		document.getElementById("message").innerHTML = msg
		}
		
	/*Evaluates UI selection based on info passed through html events ("onclick", etc.)
	  selection == api URL, specified in the relevant 'id' attribute in the html
	  cmd == friendly name of cmd we're trying to execute. You could use the 'name' attribute or text of an element.*/
	function execCom(apiCall,cmd) {
		var selection = apiCall.value //value of dropdown menu selection
		
		if (selection === undefined){ //if not a dropdown menu item
			getVCdata(apiCall,cmd)
		
			}
		else if (selection != 'null'){//catch dropdown value 'null'; if not 'null' then ...
			getVCdata(selection,cmd)
			}
	}	
				
	//HTTP get request sent to VC server. If returns result, parses & uses that data as specified.	
	function getVCdata(apiCall,item,optionalVal) {
		var val = optionalVal||'';
		var xhttp = new XMLHttpRequest();

		xhttp.onreadystatechange = function() {
			var response = xhttp.responseText;
			var regex = /<Result>(.*?)</;		
												
				if (xhttp.readyState == 4 && xhttp.status == 200) {	
					if (response.match(regex)){
						var result = regex.exec(response)[1];
						var myRange = document.getElementById(item)//for range sliders only, to find value of slider.
						if (result.indexOf("Error") == -1){
							if (parseInt(result)){//if 'result' is an int, assumes we want to update our range value
								myRange.value = result;
								UIfeedback(item+': '+result);
								}
							else {
								UIfeedback(item+': '+val)
							}
						}				

						else {//Error message
							UIfeedback(result)
							}
						}
					else {
						UIfeedback('Sent: '+item)//commands that don't return a VC result
						}
				}			
		}
		
		xhttp.open("GET", apiCall, true);
		xhttp.send();
	}
	
	//send changed slider values (range input) to VC
	function setVal(action,newVal,cmd){
		var url = action+newVal
		getVCdata(url,cmd,' '+newVal)
	}
	