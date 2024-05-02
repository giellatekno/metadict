use base64::{engine::general_purpose::URL_SAFE, DecodeError, Engine as _};

pub fn urlencode<T: AsRef<[u8]>>(input: T) -> String {
    URL_SAFE.encode(input)
}

pub fn urldecode<T: AsRef<[u8]>>(input: T) -> Result<Vec<u8>, DecodeError> {
    URL_SAFE.decode(input)
}
