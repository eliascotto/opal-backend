import { Subject } from './Subject';
export class AsyncSubject extends Subject {
    constructor() {
        super(...arguments);
        this.value = null;
        this.hasValue = false;
        this.isComplete = false;
    }
    _checkFinalizedStatuses(subscriber) {
        const { hasError, hasValue, value, thrownError, isStopped } = this;
        if (hasError) {
            subscriber.error(thrownError);
        }
        else if (isStopped) {
            hasValue && subscriber.next(value);
            subscriber.complete();
        }
    }
    next(value) {
        if (!this.isStopped) {
            this.value = value;
            this.hasValue = true;
        }
    }
    complete() {
        const { hasValue, value, isComplete } = this;
        if (!isComplete) {
            this.isComplete = true;
            hasValue && super.next(value);
            super.complete();
        }
    }
}
//# sourceMappingURL=AsyncSubject.js.map