import { BehaviorSubject } from 'rxjs';

import { parse, stringify } from 'flatted';

class LocalStorageBehaviorSubject extends BehaviorSubject {
    getValue() {
        const { hasError, thrownError, _value } = this;
        if (hasError) {
            throw thrownError;
        }
        const storedValue = localStorage.getItem(this.key);
        if (!storedValue) return null;
        return parse(storedValue);
    }

    next(value) {
        localStorage.setItem(this.key, stringify(value));
        super.next(value);
    }
}

export {LocalStorageBehaviorSubject};