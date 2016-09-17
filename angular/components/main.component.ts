import {Component, OnInit} from '@angular/core';
import {LogBox, RawEvent} from '../../models/logbox';
import {LogBoxService} from '../services/logbox.service';

@Component({
    template: '<h3>Hello world!</h3>'
})
export class Hello { }

@Component({
    template: '<h3>Its the UI-Router hello world app!</h3>'
})
export class About { }

@Component({
    selector: 'main-angular',
    providers: [LogBoxService],
    templateUrl: 'main.html'
})
export class MainComponent implements OnInit {
    title = 'Title';
    subtitle = 'Subtitle';

    logbox: LogBox;

    constructor(private logBoxService: LogBoxService) {
        console.log('Constructing LogBox');
    }

    ngOnInit(): void {
        console.log('Fetching LogBox', this.logBoxService);
        this.logBoxService.get('356156068026087').subscribe((rawEvents: RawEvent[]) => {
            this.logbox = LogBox.fromEvents(rawEvents);
            console.log(this.logbox);
        });
    }
}
