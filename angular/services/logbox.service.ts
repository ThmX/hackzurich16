import {Injectable} from '@angular/core';

import {RestService} from './rest.service';
import {RawEvent} from '../../models/logbox';

@Injectable()
export class LogBoxService {

    constructor(private rest: RestService) { }

    assets() {
        return this.rest.get<string[]>('events');
    }

    get(asset: string) {
        return this.rest.get<RawEvent[]>('events/' + asset);
    }

}