<div class="center">
    <h1>Monitoring system.</h1>
    <p>
        This is Home page for my monitoring system. Now it's configured to
        demonstrate its functionality based on weather data, but it can change
        in future. <br> 
        New features are going to be added here as they appear and ready.
    </p>

    <button onclick="window.location='http://localhost:3000';">Grafana</button>

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
        /* margin-top: 25%; */
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
