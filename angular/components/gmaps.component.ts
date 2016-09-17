import {Component, OnInit} from '@angular/core';

import {LogBox, RawEvent} from '../../models/logbox';
import {LogBoxService} from '../services/logbox.service';

@Component({
    selector: 'gmaps',
    templateUrl: 'gmaps.html',
    styleUrls: ['gmaps.css']
})
export class GMapsComponent implements OnInit {

    minDay = 1;
    maxDay = 16;

    asset: string = '356156068026087';
    fromDay: number = 2;
    toDay: number = 4;

    logbox: LogBox;

    constructor(private logBoxService: LogBoxService) {}

    ngOnInit(): void {
        console.log('Fetching LogBox', this.logBoxService);
        setTimeout(() => {
            this.updateData();
        });
    }

    updateAsset(): void {
        switch (this.asset) {
            case '356156068030410':
                this.minDay = 1;
                this.maxDay = 16;
                break;

            case '356156068026087':
                this.minDay = 5;
                this.maxDay = 16;
                break;
        }
        this.updateData();
    }

    updateData(): void {
        const now = new Date();
        if (this.fromDay < this.minDay) {
            this.fromDay = this.minDay;
        }

        if (this.toDay > this.maxDay) {
            this.toDay = this.maxDay;
        }

        const fromDate = new Date(now.getFullYear(), now.getMonth(), this.fromDay);
        const toDate = new Date(now.getFullYear(), now.getMonth(), this.toDay);
        this.logBoxService.get(this.asset, fromDate, toDate).subscribe((rawEvents: RawEvent[]) => {
            this.logbox = LogBox.fromEvents(rawEvents);
        });
    }

}
