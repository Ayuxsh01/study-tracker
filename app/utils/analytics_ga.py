"""
Injects Google Analytics (GA4) tracking into the app.

Streamlit renders pages inside its own document, and st.markdown's
unsafe_allow_html does not execute <script> tags directly. The standard
workaround is to render the tracking script inside an isolated
components.v1.html iframe, then have that iframe's JavaScript reach into
the parent page (same-origin, since both are served from the same
Streamlit app) and inject the real GA script tag into the parent's <head>.
"""

import streamlit.components.v1 as components

GA_MEASUREMENT_ID = "G-LF8P7F649Q"


def inject_google_analytics():
    components.html(
        f"""
        <script>
        (function() {{
            var doc = window.parent.document;
            if (doc.getElementById('ga-script-tag')) return;  // avoid double-injecting on reruns

            var gaScript = doc.createElement('script');
            gaScript.id = 'ga-script-tag';
            gaScript.async = true;
            gaScript.src = 'https://www.googletagmanager.com/gtag/js?id={GA_MEASUREMENT_ID}';
            doc.head.appendChild(gaScript);

            var inlineScript = doc.createElement('script');
            inlineScript.id = 'ga-inline-tag';
            inlineScript.innerHTML = `
                window.dataLayer = window.dataLayer || [];
                function gtag(){{ dataLayer.push(arguments); }}
                gtag('js', new Date());
                gtag('config', '{GA_MEASUREMENT_ID}');
            `;
            doc.head.appendChild(inlineScript);
        }})();
        </script>
        """,
        height=0,
        width=0,
    )
