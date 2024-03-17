import http from "k6/http";
import { check } from "k6";

export const options = {
  stages: [
    { target: 200, duration: "30s" },
    { target: 0, duration: "30s" },
  ],
};

export default function () {
  const body = {
    tracker: {
      WINDOW_LOCATION_HREF:
        "https://polytech.univ-cotedazur.fr/ecole/association-alumni",
      USER_AGENT: "Mozilla/5.0",
      PLATFORM: "Windows 11 Pro x64",
      TIMEZONE: "UTC+01:00",
    },
  };

  const postResult2 = http.post(
    "http://polymetrie-polymetrie-chart:5000/api/visits",
    JSON.stringify(body),
    { headers: { "Content-Type": "application/json" } }
  );
  check(postResult2, {
    "http response status code is 201": postResult2.status === 201,
  });
}
