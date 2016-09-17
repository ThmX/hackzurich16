import {NgModule} from '@angular/core';
import {FormsModule} from '@angular/forms';
import {HttpModule} from '@angular/http';
import {BrowserModule} from '@angular/platform-browser';

import {MainComponent}  from './components/main.component';
import {routing, routingDeclarations, routingProviders} from './main.routing';
import {HighlightDirective} from './directives/highlight.directive';
import {LocalStorageService, SessionStorageService} from './services/storage.service';
import {RestService} from './services/rest.service';
import {UserService} from './services/user.service';

@NgModule({
    imports: [
        BrowserModule,
        FormsModule,
        HttpModule,
        routing
    ],
    declarations: [
        ...routingDeclarations,
        MainComponent,
        HighlightDirective
    ],
    providers: [
        routingProviders,
        LocalStorageService,
        SessionStorageService,
        RestService,
        UserService
    ],
    bootstrap: [
        MainComponent
    ]
})
export class MainModule { }
