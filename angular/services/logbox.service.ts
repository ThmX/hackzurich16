import {Injectable} from '@angular/core';

import * as dateformat from 'dateformat';

import {RestService} from './rest.service';
import {RawEvent} from '../../models/logbox';

const restDateFormat = 'yyyy-mm-dd';

@Injectable()
export class LogBoxService {

    constructor(private rest: RestService) {}

    assets() {
        return this.rest.get<string[]>('events');
    }

    get(asset: string, fromDate: Date, toDate?: Date) {
        let url = 'events/' + asset + '/' + dateformat(fromDate, restDateFormat);
        if (toDate) {
            url += '/' + dateformat(toDate, restDateFormat);
        }
        return this.rest.get<RawEvent[]>(url);
    }

}