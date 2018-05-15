$(function() {
    $('#product-form').submit(function (e) {
        // e.preventDefault();
        e.stopImmediatePropagation()
        var primary_image_file = document.getElementById("id_primary_image_file").files[0];
        if(primary_image_file){
            getSignedRequest(primary_image_file, function (url) {
                console.log("ZDAROVA IZ SOLYANOVA");
                document.getElementById("id_primary_image").value = url
            });
        }

        var images_files = document.getElementById("id_images_files").files;
        if(images_files.length) {
            var tempArray = [];
            for (var i = 0; i < images_files.length; i++) {
                getSignedRequest(images_files[i], function (url) {
                    console.log("ZDAROVA IZ SOLYANOVA VERSION 20");
                    tempArray.push(url)
                });
            }
            $("#id_images").val(JSON.stringify(tempArray))
        }
        return true;
    });
});

function getSignedRequest(file, onSuccess){
  var xhr = new XMLHttpRequest();
  xhr.open("GET", "api/sign_s3?file_name="+file.name+"&file_type="+file.type, false);
  xhr.send();

  if(xhr.status === 200){
    var response = JSON.parse(xhr.responseText);
    uploadFile(file, response.data, response.url, onSuccess);
  }
  else{
    alert("Could not get signed URL.");
  }

}

function uploadFile(file, s3Data, url, onSuccess){
  var xhr = new XMLHttpRequest();
  xhr.open("POST", s3Data.url, false);

  var postData = new FormData();
  console.log(s3Data.fields)
  for(key in s3Data.fields){
      postData.append(key, s3Data.fields[key]);
  }
  postData.append('file', file);
  console.log(postData);

  xhr.send(postData);
  if(xhr.status === 200 || xhr.status === 204){
     onSuccess(url)
  }
  else{
    alert("Could not upload file.");
  }
}


