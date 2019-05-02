
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
            
            // [
            //     {lat: 7.8731, lng: 80.7718, slide: 'RIGHT_ROUND'},//Sri Lanka
            //     {lat: -25.2744, lng: 133.7751, slide: 'LEFT_ROUND'},//Australia
            //     {lat: 36.2048, lng: 138.2529}//Japan
            // ]
            // [
            //     {lat: 7.8731, lng: 80.7718, slide: 'RIGHT_ROUND'},//Sri Lanka
            //     {lat: 3.1390, lng: 101.6869}
            // ],
            // [
            //     {lat: 7.8731, lng: 80.7718, slide: 'RIGHT_ROUND',deep:"8"},//Sri Lanka
            //     {lat: 41.8719, lng: 12.5674}
            // ],
            // [
            //     {lat: -25.2744, lng: 133.7751},//Australia
            //     {lat: 36.9006, lng: 138.8860}//Japan
            // ],
            // [
            //     {lat: 7.8731, lng: 80.7718, slide: 'RIGHT_ROUND'},
            //     {lat: -18.7669, lng: 46.8691},
            // ]
        ,

        icon: {
            path: "plane.png"
        }
    }, dash_straight).addTo(map);

}

//DOCUMENT READY
$(function () {

    var map = L.map('map').setView([40.9270786, -79.861243], 3);
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

    L.bezier({
        path: [
            [
                {lat: 7.8731, lng: 80.7718, slide: 'RIGHT_ROUND'},//Sri Lanka
                {lat: -25.2744, lng: 133.7751, slide: 'LEFT_ROUND'},//Australia
                {lat: 36.2048, lng: 138.2529}//Japan
            ]
            // [
            //     {lat: 7.8731, lng: 80.7718, slide: 'RIGHT_ROUND'},//Sri Lanka
            //     {lat: 3.1390, lng: 101.6869}
            // ]
        ],

        icon: {
            path: "plane.png"
        }
    }, dash_straight).addTo(map);


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
        // var testarr = $('select:has(option[value="A1"]:selected)');
        console.log(jsonObj)
        
        $.ajax({
            type:"POST",    
            url: "http://localhost:5000/test",
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify(jsonObj),
                success: function(result, status){
                // $("#div1").html(result);
                // console.log(status)
                console.log(result)
                reloadMap(map, result)
                }
        });
    })



});