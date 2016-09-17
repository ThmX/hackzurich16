import {Injectable} from '@angular/core';

import {RestService} from './rest.service';
import {User} from '../../models/user';

@Injectable()
export class UserService {

    constructor(private rest: RestService) { }

    all() {
        return this.rest.get<User[]>('users');
    }

    get(id: number) {
        return this.rest.get<User>('user/' + id);
    }

    create(id: number, user: User) {
        return this.rest.post<User>('user/' + id, user);
    }

    edit(id: number, user: User) {
        return this.rest.put<User>('user/' + id, user);
    }

    delete(id: number) {
        return this.rest.delete('user/' + id);
    }

}