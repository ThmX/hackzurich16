import {NgModule} from '@angular/core';
import {FormsModule} from '@angular/forms';
import {HttpModule} from '@angular/http';
import {BrowserModule} from '@angular/platform-browser';

import {AgmCoreModule} from 'angular2-google-maps/core';


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
        AgmCoreModule.forRoot({
            apiKey: 'AIzaSyCRVK9f_J4IhW5B0JL4zH0HK0jbm16ka-U'
        }),
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
