
   
function send(values){
	$.ajax({
		 url: "http://192.168.0.42:8080",
		 async: false, // jsonp requests cannot be synchronous!
		 type: 'POST',
		 contentType:"application/json; charset=utf-8",
		 data: JSON.stringify(values),
		 dataType: "json"
		});
}


function get_initial_values(){

    console.log("test");

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "http://192.168.0.42:8080");
    xhr.setRequestHeader("Accept", "application/json");
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = function () {
       if (xhr.readyState === 4) {
          console.log(xhr.status);
          console.log(xhr.responseText);
          obj = JSON.parse(xhr.responseText);
          set_initial_values(obj)
       }};

    var data = `{
      "Mode": "read_values"
    }`;

    xhr.send(data);


    }


function set_initial_values(value){

    document.getElementById('Setting_1_An').value = obj.Time_Settings.setting_1.on;
    document.getElementById('Setting_1_Aus').value = obj.Time_Settings.setting_1.off;
    document.getElementById('Setting_2_An').value = obj.Time_Settings.setting_2.on;
    document.getElementById('Setting_2_Aus').value = obj.Time_Settings.setting_2.off;
    document.getElementById('randomtime').value = obj.random_changeTime;


    document.getElementById('Veranda_Aus').checked = true;
    document.getElementById('Vordach_Aus').checked = true;
    document.getElementById('LichtOben_Aus').checked = true;
    document.getElementById('LichtUnten_Aus').checked = true;
    document.getElementById('Steckdosen_Aus').checked = true;
}