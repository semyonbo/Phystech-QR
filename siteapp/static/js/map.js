ymaps.ready(init);
var myMap;
var myPlacemark;

function init() {

    myMap = new ymaps.Map("map", {
        center: [59.927301, 30.338456],
        zoom: 16,
        controls: [],

    }, {
        yandexMapDisablePoiInteractivity: true,
        suppressMapOpenBlock: true,
        suppressObsoleteBrowserNotifier: true,
        balloonMaxWidth: 200,
    });
    myMap.events.add('click', function (e) {
        if (!myMap.balloon.isOpen()) {
            var coords = e.get('coords');
            document.getElementById('geo_inp').value = [
                coords[0].toPrecision(6),
                coords[1].toPrecision(6)
            ].join(', ');
        } else {
            myMap.balloon.close();
        }
        if (myPlacemark) {
            myPlacemark.geometry.setCoordinates(coords);
        } else {
            myPlacemark = createPlacemark(coords);
            myMap.geoObjects.add(myPlacemark);
            myPlacemark.events.add('dragend', function () {
                getAddress(myPlacemark.geometry.getCoordinates());
            });
        }
        getAddress(coords);
        myPlacemark.events.add('dragend', function () {
            getAddress(myPlacemark.geometry.getCoordinates());
            console.log(myPlacemark.geometry.getCoordinates());
            document.getElementById('geo_inp').value = [
                myPlacemark.geometry.getCoordinates()[0].toPrecision(6),
                myPlacemark.geometry.getCoordinates()[1].toPrecision(6)
            ].join(', ');
        });
    });


    function createPlacemark(coords) {
        return new ymaps.Placemark(coords, {
            iconCaption: 'поиск...'
        }, {
            preset: 'islands#violetDotIconWithCaption',
            draggable: true
        });
    }

    function getAddress(coords) {
        myPlacemark.properties.set('iconCaption', 'поиск...');
        ymaps.geocode(coords).then(function (res) {
            var firstGeoObject = res.geoObjects.get(0);

            myPlacemark.properties
                .set({
                    iconCaption: [
                        firstGeoObject.getLocalities().length ? firstGeoObject.getLocalities() : firstGeoObject.getAdministrativeAreas(),
                        firstGeoObject.getThoroughfare() || firstGeoObject.getPremise()
                    ].filter(Boolean).join(', '),
                    balloonContent: firstGeoObject.getAddressLine()
                });
        });
    }
}
