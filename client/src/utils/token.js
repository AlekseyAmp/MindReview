export function decodeJWT(token) {
    const [headerEncoded, payloadEncoded] = token.split('.');

    const decodedHeader = JSON.parse(atob(headerEncoded));
    const decodedPayload = JSON.parse(atob(payloadEncoded));

    return { header: decodedHeader, payload: decodedPayload };
}
