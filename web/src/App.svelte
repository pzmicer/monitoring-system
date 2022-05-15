<script>
    let grafana_url = GRAFANA_URL;

    function toGrafana() {
        console.log(grafana_url);
        // window.location = grafana_url;
    }
</script>

<svelte:head>
    <title>Monitoring system</title>
</svelte:head>

<div class="center">
    <!-- <h1>Monitoring system</h1> -->
    <!-- <h1>{grafana_url}</h1> -->
    <h1>{grafana_url} asd</h1>
    <p>
        This is Home page for monitoring system. Now it's configured for weather
        data, but it can be changed in future.
        <br />
        Current weather data include fields like temperature, wind speed and pressure.
        New fields can also be added, as well as not only weather data can be stored.
        <br />
        New features are going to be added here as they appear and ready.
    </p>

    <!-- <button onclick="window.location='http://localhost:3000';">Grafana</button> -->
    <button on:click={toGrafana}>Grafana</button>

    <footer>
        GitHub: <a href="https://github.com/pzmicer/monitoring-system"
            >https://github.com/pzmicer/monitoring-system</a
        >
    </footer>
</div>

<style>
    p {
        font-size: 14pt;
        text-align: center;
        line-height: 200%;
    }

    button {
        font-size: 20pt;
        margin: 5%;
    }

    .center {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    footer {
        text-align: center;
        border-top: 1px solid #000;
        display: inline-block;
        padding: 20px;

        position: fixed;
        bottom: 50px;
    }
</style>
