import { __extends } from "tslib";
import { Subject } from './Subject';
var AsyncSubject = (function (_super) {
    __extends(AsyncSubject, _super);
    function AsyncSubject() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.value = null;
        _this.hasValue = false;
        _this.isComplete = false;
        return _this;
    }
    AsyncSubject.prototype._checkFinalizedStatuses = function (subscriber) {
        var _a = this, hasError = _a.hasError, hasValue = _a.hasValue, value = _a.value, thrownError = _a.thrownError, isStopped = _a.isStopped;
        if (hasError) {
            subscriber.error(thrownError);
        }
        else if (isStopped) {
            hasValue && subscriber.next(value);
            subscriber.complete();
        }
    };
    AsyncSubject.prototype.next = function (value) {
        if (!this.isStopped) {
            this.value = value;
            this.hasValue = true;
        }
    };
    AsyncSubject.prototype.complete = function () {
        var _a = this, hasValue = _a.hasValue, value = _a.value, isComplete = _a.isComplete;
        if (!isComplete) {
            this.isComplete = true;
            hasValue && _super.prototype.next.call(this, value);
            _super.prototype.complete.call(this);
        }
    };
    return AsyncSubject;
}(Subject));
export { AsyncSubject };
//# sourceMappingURL=AsyncSubject.js.map