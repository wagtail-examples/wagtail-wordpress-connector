class ShowMessage {
    constructor(times=3) {
        this.message = 'Hello from Wagtail starter kit!';
        this.times = times;
    }

    showMessage() {
        for (let i = 0; i < this.times; i++) {
            console.log(this.message);
        }
    }
}

const showMessage = new ShowMessage();
showMessage.showMessage();
