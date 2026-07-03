NEW_CONNECTION = "انشعاب جدید"

AFTER_SALE = "خدمات پس از فروش"

METER_TEST = "آزمایش و تست کنتور"

BILL = "بررسی قبض برق"


ALLOWED_IDENTIFIERS = {

    NEW_CONNECTION: [

        "REQUEST_NO",

        "MOBILE",

        "NATIONAL_CODE"

    ],

    AFTER_SALE: [

        "REQUEST_NO",

        "MOBILE",

        "NATIONAL_CODE",

        "COMPUTER_CODE",

        "BILL_ID"

    ],

    METER_TEST: [

        "REQUEST_NO",

        "MOBILE",

        "NATIONAL_CODE",

        "COMPUTER_CODE",

        "BILL_ID"

    ],

    BILL: [

        "MOBILE",

        "COMPUTER_CODE",

        "BILL_ID"

    ]

}
