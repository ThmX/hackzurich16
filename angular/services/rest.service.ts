import {Injectable} from '@angular/core';
import {Http, Response, RequestOptionsArgs} from '@angular/http';
import {Observable} from 'rxjs';
import 'rxjs/add/operator/map';

import {LocalStorageService} from './storage.service';

@Injectable()
export class RestService {

    static JWT_KEY = 'JWT_KEY';

    private jwt: string;
    private base: string;

    constructor(
        private http: Http,
        private localStorageService: LocalStorageService
    ) {
        this.base = '';

        this.reloadJWT();
    }

    private reloadJWT(): void {
        this.localStorageService.getOrElse(RestService.JWT_KEY, 'abc').subscribe(
            (jwt: string) => this.jwt = jwt
        );
    }

    private static extractData<T>(res: Response): T {
        return res.json();
    }

    private static handleError(error: any) {
        // In a real world app, we might use a remote logging infrastructure
        // We'd also dig deeper into the error to get a better message
        let errMsg = (error.message) ? error.message :
            error.status ? `${error.status} - ${error.statusText}` : 'Server error';
        console.error(errMsg); // log to console instead
        return Observable.throw(errMsg);
    }

    get<T>(url: string, options?: RequestOptionsArgs): Observable<T> {
        return this.http.get(this.base + url, options)
            .map(RestService.extractData)
            .catch(RestService.handleError) as Observable<T>;
    }

    post<T>(url: string, body: any, options?: RequestOptionsArgs): Observable<T> {
        return this.http.post(this.base + url, body, options)
            .map(RestService.extractData)
            .catch(RestService.handleError) as Observable<T>;
    }

    put<T>(url: string, body: any, options?: RequestOptionsArgs): Observable<T> {
        return this.http.put(this.base + url, body, options)
            .map(RestService.extractData)
            .catch(RestService.handleError) as Observable<T>;
    }

    delete(url: string, options?: RequestOptionsArgs): Observable<boolean> {
        return this.http.delete(this.base + url, options)
            .map(RestService.extractData)
            .catch(RestService.handleError) as Observable<boolean>;
    }

}