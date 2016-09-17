export class Event {

    constructor(
        public id: number,
        public asset: string,
        public recorded_at: string,
        public received_at: string,
        public loc: any,
        public connection_id: number,
        public index: number,
        public fields: any
    ) {}

}