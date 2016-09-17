import {Injectable} from '@angular/core';
import {Observable} from 'rxjs';

export class ProxyStorage {

    constructor(public storage: Storage | InMemoryStorage) {}

    private getInternal<T>(key: string): T {
        const value = this.storage.getItem(key);
        return value ? JSON.parse(value) as T : undefined;
    }

    get<T>(key: string): Observable<T> {
        return Observable.of(this.getInternal(key)) as Observable<T>;
    }

    getOrElse<T>(key: string, orElse: (() => Observable<T>) | (() => T) | T): Observable<T> {
        const tmp = this.getInternal(key);
        if (tmp) {
            return Observable.of(tmp) as Observable<T>;
        }

        if (orElse instanceof Function) {
            const orElseValue = orElse();
            if (orElseValue instanceof Observable) {
                const obs: Observable<T> = orElseValue;
                obs.subscribe((t: T) => {
                    this.set(key, t);
                });
                return obs;

            } else {

                const value: T = orElseValue;
                this.set(key, value);
                return Observable.of(value);
            }
        }

        const value: T = orElse;
        this.set(key, value);
        return Observable.of(value);
    }

    set<T>(key: string, data: T): void {
        this.storage.setItem(key, JSON.stringify(data));
    }

    remove(key: string): void {
        this.storage.removeItem(key);
    }

    clear(): void {
        this.storage.clear();
    }
}

export class InMemoryStorage {

    private mem = {};

    clear(): void {
        this.mem = {};
    }

    getItem(key: string): any {
        return key in this.mem ? this.mem[key] : undefined;
    }

    key(index: number): string {
        return Object.keys(this.mem)[index];
    }

    removeItem(key: string): void {
        if (key in this.mem) {
            delete this.mem[key];
        }
    }

    setItem(key: string, data: string): void {
        this.mem[key] = data;
    }
}

@Injectable()
export class LocalStorageService extends ProxyStorage {
    constructor() {
        if (localStorage) {
            super(localStorage);
        } else {
            super(new InMemoryStorage());
            console.log("Warning: localStorage couldn't be localized.");
        }
    }
}

@Injectable()
export class SessionStorageService extends ProxyStorage {
    constructor() {
        if (sessionStorage) {
            super(sessionStorage);
        } else {
            super(new InMemoryStorage());
            console.log("Warning: sessionStorage couldn't be localized.");
        }
    }
}