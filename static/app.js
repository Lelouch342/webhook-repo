let displayedEventIds = new Set();

async function fetchEvents() {

    try {

        const response = await fetch("/events");
        const data = await response.json();

        const container = document.getElementById("events-container");

        data.reverse().forEach(event => {

            if (displayedEventIds.has(event.id)) return;

            const formattedText = formatEvent(event);

            const div = document.createElement("div");
            div.className = "event";
            div.innerText = formattedText;

            container.prepend(div);

            displayedEventIds.add(event.id);
        });

    } catch (error) {
        console.error("Polling error:", error);
    }
}

function formatEvent(event) {

    const date = new Date(event.timestamp);

    const formattedTime = date.toUTCString().replace("GMT", "UTC");

    if (event.action === "PUSH") {
        return `${event.author} pushed to ${event.to_branch} on ${formattedTime}`;
    }

    if (event.action === "PULL_REQUEST") {
        return `${event.author} submitted a pull request from ${event.from_branch} to ${event.to_branch} on ${formattedTime}`;
    }

    if (event.action === "MERGE") {
        return `${event.author} merged branch ${event.from_branch} to ${event.to_branch} on ${formattedTime}`;
    }

    return "";
}

// Initial fetch
fetchEvents();

// Poll every 15 seconds
setInterval(fetchEvents, 15000);
