
function reloadMap(map, coords){

    // console.log(map)
    //remove all layer n refresh 
    map.eachLayer(function (layer) {
        // console.log(layer._url)
        if( !layer._url){
            map.removeLayer(layer)
        }
    });
    
    var dash_straight = {
        color: 'rgb(145, 146, 150)',
        fillColor: 'rgb(145, 146, 150)',
        dashArray: 8,
        opacity: 0.8,
        weight: '1',
    };

    //L.vezier returnb L.layerGroup(paths);
    //reload and send with right longitute latitudes
    L.bezier({
        path: coords
        ,

        icon: {
            path: "plane.png"
        }
    }, dash_straight).addTo(map);

}

function drawMarkers(map, markerCoords){
    console.log(markerCoords)
    setTimeout(function(){
    
    markerCoords.forEach( function(arr){
    
    var marker = L.marker([arr[1]["lat"],arr[1]["lng"]])
        
    pricePopup = "<b>"+"Destination:"+arr[2].toString()+"</b>"+"<div>"+"$" + arr[0].toString()+"</div>"
    
    marker.bindPopup(pricePopup).openPopup();

    marker.addTo(map)


    })

    },5500)
}

function getFlaskData(map,jsonObj){
$.ajax({
    type:"POST",    
    url: "http://localhost:5000/test",
    contentType: 'application/json;charset=UTF-8',
    data: JSON.stringify(jsonObj),
        success: function(result, status){
        // $("#div1").html(result);
        // console.log(status)
        // console.log(result)
        reloadMap(map, result)},
        complete:function(){
            $.ajax({
                type:"POST",    
                url: "http://localhost:5000/get_prices",
                contentType: 'application/json;charset=UTF-8',
                data: JSON.stringify(jsonObj),
                    success: function(result, status){
                    // $("#div1").html(result);
                    drawMarkers(map,result)
                    // console.log("@2nd ajax")
                    // console.log(result)                    
                }
        });
        }
        
    });
}



//DOCUMENT READY
$(function () {

    var map = L.map('map').setView([45.9270786, -88.861243], 4);

    map.scrollWheelZoom.disable();
    map.on('zoomend',function(){
        getFlaskData(map,testingObj)
    });
    map.on('moveend',function(){
        getFlaskData(map,testingObj)
    });

    L.tileLayer('https://cartodb-basemaps-c.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png', {
        maxZoom: 18,
        id: 'mapbox.streets'
    }).addTo(map);
    var dash_straight = {
        color: 'rgb(145, 146, 150)',
        fillColor: 'rgb(145, 146, 150)',
        dashArray: 8,
        opacity: 0.8,
        weight: '1',
    };

    // L.bezier({
    //     path: [
    //         [
    //             {lat: 7.8731, lng: 80.7718, slide: 'RIGHT_ROUND'},//Sri Lanka
    //             {lat: -25.2744, lng: 133.7751, slide: 'LEFT_ROUND'},//Australia
    //             {lat: 36.2048, lng: 138.2529}//Japan
    //         ]
    //         // [
    //         //     {lat: 7.8731, lng: 80.7718, slide: 'RIGHT_ROUND'},//Sri Lanka
    //         //     {lat: 3.1390, lng: 101.6869}
    //         // ]
    //     ],

    //     icon: {
    //         path: "plane.png"
    //     }
    // }, dash_straight).addTo(map);

    let testingObj;
    $("#select-options").on("change", function(){
        console.log("on change")
        var quarter = $(this).children()[0].value
        var year = $(this).children()[1].value
        var city = $(this).children()[2].value

        jsonObj = {
            "quarter": quarter,
            "year": year,
            "city": city
        }
        testingObj = jsonObj

        // var testarr = $('select:has(option[value="A1"]:selected)');
        console.log(testingObj)
        getFlaskData(map,jsonObj)
        
    })



});