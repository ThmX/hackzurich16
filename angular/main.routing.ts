import {Routes, RouterModule} from '@angular/router';
import {ModuleWithProviders} from '@angular/core';
import {GMapsComponent} from './components/gmaps.component';
import {AboutComponent} from './components/about.component';
import {StatsComponent} from './components/stats.component';
import {StatsBarComponent} from './components/stats.bar.component';
import {StatsLineComponent} from './components/stats.line.component';

const appRoutes: Routes = [
    { path: '', redirectTo: '/maps', pathMatch: 'full' },
    { path: 'maps', component: GMapsComponent },
    { path: 'stats', component: StatsComponent },
    { path: 'about', component: AboutComponent }
];

export const routingProviders: any[] = [

];

export const routingDeclarations: any[] = [
    GMapsComponent,
    StatsComponent,
    StatsBarComponent,
    StatsLineComponent,
    AboutComponent,
];

export const routing: ModuleWithProviders = RouterModule.forRoot(appRoutes, { useHash: true });
