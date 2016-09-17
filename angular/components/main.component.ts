import {Component} from '@angular/core';

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
    templateUrl: 'main.html'
})
export class MainComponent {
    title = 'Title';
    subtitle = 'Subtitle';
}
