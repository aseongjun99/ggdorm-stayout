import * as cheerio from "cheerio";

export function getInputValue(html, name) {
    const $ = cheerio.load(html);
    return $(`input[name="${name}"]`).attr("value") ?? "";
}