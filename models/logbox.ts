import * as _ from 'lodash';

export class RawEvent {

    constructor(
        public id: number,
        public asset: string,
        public recorded_at: string,
        public received_at: string,
        public loc: number[],
        public connection_id: number,
        public index: number,
        public fields: (any[])
    ) {}

}

export class LBCoord {

    constructor(
        public long: number,
        public lat: number
    ) {}

    static fromArray(arr: number[]): LBCoord {
        if (arr) {
            const [long, lat] = arr;
            return new LBCoord(long, lat);
        }
    }
}

export class LBField {

    constructor(
        public key: string,
        public value: any
    ) {}

    asString(): string {
        return this.value as string;
    }

    asBoolean(): boolean {
        return this.value as boolean;
    }

    asNumber(): number {
        return this.value as number;
    }

}

export class LBEvent {

    constructor(
        public id: number,
        public recorded_at: Date,
        public received_at: Date,
        public location: LBCoord,
        public connection_id: number,
        public index: number,
        public fields: LBField[]
    ) {}

    static fromRaw(raw: RawEvent): LBEvent {
        return new LBEvent(
            raw.id,
            new Date(raw.recorded_at),
            new Date(raw.received_at),
            LBCoord.fromArray(raw.loc),
            raw.connection_id,
            raw.index,
            _.map(raw.fields, (value: any, key: string) => new LBField(key, value))
        );
    }

}

export class LogBox {

    constructor(
        public asset: string,
        public location: LBCoord,
        public events: LBEvent[]
    ) {}

    trace(): LBEvent[] {
        return _.filter(this.events, evt => evt.location);
    }

    static fromEvents(events: RawEvent[]): LogBox {
        if (events) {
            let evt = _.find(events, (evt: RawEvent) => evt.loc);
            if (!evt) {
                evt = _.first(events);
            }

            return new LogBox(
                evt.asset,
                LBCoord.fromArray(evt.loc),
                _.map(events, LBEvent.fromRaw)
            );

        }
    }
}