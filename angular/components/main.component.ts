import {Component} from '@angular/core';
import {LogBoxService} from '../services/logbox.service';

@Component({
    selector: 'main-angular',
    providers: [LogBoxService],
    templateUrl: 'main.html',
    styleUrls: ['main.css']
})
export class MainComponent {
    title = 'Title';
    subtitle = 'Subtitle';
}
