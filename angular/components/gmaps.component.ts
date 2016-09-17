import {Component} from '@angular/core';
import {LogBox} from '../../models/logbox';
import {Input} from '@angular/core';

@Component({
    selector: 'gmaps',
    templateUrl: 'gmaps.html',
    styleUrls: ['gmaps.css']
})
export class GMapsComponent {

    @Input() logBox: LogBox;

}
