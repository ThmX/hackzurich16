import {Component} from '@angular/core';
import {GPSCoord} from "../../models/gps.coord";

@Component({
    selector: 'gmaps',
    templateUrl: 'gmaps.html',
    styleUrls: ['gmaps.css']
})
export class GMapsComponent {
    location = new GPSCoord(47.3775499, 8.4666748);

    trace = [
        new GPSCoord(47.3775499, 8.4666748),
        new GPSCoord(49.3775499, 8.4666748),
        new GPSCoord(52.3775499, 6.4666748),
        new GPSCoord(47.3775499, 5.4666748),
        new GPSCoord(47.3775499, 8.4666748)
    ]
}
