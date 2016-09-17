import {Routes, RouterModule} from '@angular/router';
import {ModuleWithProviders} from '@angular/core';
import {Hello, About} from './components/main.component';

const appRoutes: Routes = [
    { path: '', redirectTo: '/hello', pathMatch: 'full' },
    { path: 'hello', component: Hello },
    { path: 'about', component: About }
];

export const routingProviders: any[] = [

];

export const routingDeclarations: any[] = [
    About,
    Hello
];

export const routing: ModuleWithProviders = RouterModule.forRoot(appRoutes, { useHash: true });
