var apigClient = apigClientFactory.newClient();

function submitPhoto() {
    //console.log("This is submit upload function");
    var inputfilespath = document.getElementById("input-file").value;
    var file = document.getElementById("input-file").files[0];
    //console.log(inputfilespath);
    //console.log(file);
    var filename = file.name;
    var filetype = file.type;
    var reader = new FileReader();
    document.getElementById('input-file').value = "";
    if ((inputfilespath == "") || (!['png', 'jpg', 'jpeg', 'txt'].includes(inputfilespath.split(".")[1]))) {
        alert("NOT a picture!");
    }
    else {
        var params = {
            item: filename,
            bucket: 'assignment2testtxt',
        };
        var additionalParams = {
        };
        document.getElementById('input-file').value = "";
        reader.onload = function (event) {
            body =  btoa(event.target.result);
            console.log(body);
            return apigClient.uploadBucketItemPut(params,body,{})
            .then(function(result){
              console.log(result);
            })
            .catch(function(error){
              console.log(error);
            });
          }
          reader.readAsBinaryString(file);
        }

}

function submitSearch() {
    console.log("This is submit search function");
    var inputsearchlabels = document.getElementById("transcript").value;
    var inputsearchinnerhtml = document.getElementById("transcript").innerHTML;
    console.log(inputsearchlabels);
    var params = {
        'label': inputsearchlabels
    };
    apigClient.searchGet(params, {}, {})
        .then(function (result) {
            console.log("Result: ", result);

        })
        .catch(function (result) {
            console.log(result);
        });
}