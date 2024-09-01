
// api status

async function getStatus(){
    const url = "http://127.0.0.1:5000/api/v1/status";
    try {
        const resp = await fetch(url);
        if (!resp.ok) {
            throw new Error(`Response status: ${resp.status}`)
        }
        const json = await resp.json();
        console.log(json);
    } catch (err){
        console.error(err.message)
    }
}
getStatus();
