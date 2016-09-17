import { Directive, ElementRef, Renderer } from '@angular/core';

import * as _ from 'lodash';

@Directive({ selector: '[highlight]' })
export class HighlightDirective {
    constructor(renderer: Renderer, el: ElementRef) {
        renderer.setElementStyle(el.nativeElement, 'backgroundColor', 'gold');
        console.log(`* AppRoot highlight called for ${el.nativeElement.tagName}`);
        console.log('lodash version ' + _.VERSION);
    }
}
