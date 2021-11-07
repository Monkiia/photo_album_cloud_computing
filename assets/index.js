var apigClient = apigClientFactory.newClient();

const getBase64fromFile = (file) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => {
        console.log(`getBase64fromFile success.`);
        const spliced = reader.result.split(',');
        const header = spliced[0];
        spliced.shift();
        resolve({
          header: header,
          body: spliced.join('')
        });
      };
      reader.onerror = (err) => {
        console.log(`getBase64fromFile failed.`);
        reject(err);
      };
    });
  }

function submitPhoto() {
    //console.log("This is submit upload function");
    var inputfilespath = document.getElementById("input-file").value;
    var file = document.getElementById("input-file").files[0];
    //console.log(inputfilespath);
    //console.log(file);
    var filename = file.name;
    var filetype = file.type;
    var reader = new FileReader();
    console.log("see see");
    console.log(file);
    document.getElementById('input-file').value = "";
    var totaldata = "";
    var labels = document.getElementById("labels").value;
    if ((inputfilespath == "") || (!['png', 'jpg', 'jpeg', 'txt'].includes(inputfilespath.split(".")[1]))) {
        alert("NOT a picture!");
    }
    else {
        var params = {
            'item': filename,
            'bucket': 'indexphotos-b2',
            'customer_labels' : labels
        };
        var additionalParams = {
        };
        document.getElementById('input-file').value = "";
        /*
        getBase64fromFile(file)
        .then(result =>
            params = {
                'item': filename,
                'bucket': 'assignment2testtxt',
                'customer_labels' : result
            })
        .then(result =>
        apigClient.lambdaUploadPut(params,result,additionalParams));
        */

        //var totaldata;
        //console.log(data);
        
        reader.onload = function (event) {
            data = btoa(event.target.result);
            //trucdata = data.split("base64,")[1];
            //totaldata = totaldata + trucdata;
            trucdata = data;
            console.log(trucdata);
            
            body = trucdata;
            totaldata = totaldata + trucdata;
            //console.log(body);
            return apigClient.lambdaPostPost(params,body,additionalParams)
            .then(function(result){
              console.log(result);
            })
            .catch(function(error){
              console.log(error);
            })
            /*
             body =  btoa(event.target.result);
            var newbody = body.split("base64,")[1];
            console.log(body);
            return apigClient.uploadBucketItemPut(params,newbody,{})
            .then(function(result){
              console.log(result);
            })
            .catch(function(error){
              console.log(error);
            });  
            //console.log(reader.result);
            //apigClient.uploadBucketItemPut(params,reader.result,{})
            */
        }
        reader.readAsBinaryString(file);
        //console.log(totaldata);
        }
        
}

function submitSearch() {
    var serachresults = [];
    var photosDiv = document.getElementById("imgDiv");
    photosDiv.innerHTML="";
    console.log("This is submit search function");
    var inputsearchlabels = document.getElementById("transcript").value;
    var inputsearchinnerhtml = document.getElementById("transcript").innerHTML;
    console.log(inputsearchlabels);
    var params = {
        'label': inputsearchlabels
    };
    
    apigClient.searchGet(params, {}, {})
        .then(function (result) {
            var n;
            files = result['data'];
            for (n = 0; n < files.length; n++) {
                console.log(files[n]);
                img = document.createElement('img');
                img.src = "https://indexphotos-b2.s3.amazonaws.com/" + files[n];
                photosDiv.appendChild(img);
            }
            //console.log("Result: ", result.data);
        })
        .catch(function (result) {
            console.log(result);
        })
    console.log("display");
    serachresults.forEach(element => {
        console.log(element);
    });
}