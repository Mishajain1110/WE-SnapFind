//! moment.js locale configuration

;(function (global, factory) {
    typeof exports === 'object' && typeof module !== 'undefined'
        && typeof require === 'function' ? factory(require('../moment')) :
    typeof define === 'function' && define.amd ? define(['../moment'], factory) :
    factory(global.moment)
 }(this, (function (moment) { 'use strict';

     var th = moment.defineLocale('th', {
         months : 'January_February_March_April_May_June_July_August_September_October_November_December'.split('_'),
         monthsShort : 'Jan._Feb._Mar._Apr._May._Jun._Jul._Aug._Sep._Oct._Nov._Dec.'.split('_'),
         monthsParseExact: true,
         weekdays : 'Sunday_Monday_Tuesday_Wednesday_Thursday_Friday_Saturday'.split('_'),
         weekdaysShort : 'Sun._Mon._Tue._Wed._Thu._Fri._Sat.'.split('_'), // yes, three characters difference
         weekdaysMin : 'Sun._Mon._Tue._Wed._Thu._Fri._Sat.'.split('_'),
         weekdaysParseExact : true,
         longDateFormat : {
             LT : 'H:mm',
             LTS : 'H:mm:ss',
             L : 'DD/MM/YYYY',
             LL : 'D MMMM YYYY',
             LLL : 'D MMMM YYYY at H:mm',
             LLLL : 'dddd, D MMMM YYYY at H:mm'
         },
         meridiemParse: /AM|PM/,
         isPM: function (input) {
             return input === 'PM';
         },
         meridiem : function (hour, minute, isLower) {
             if (hour < 12) {
                 return 'AM';
             } else {
                 return 'PM';
             }
         },
         calendar : {
             sameDay : '[Today at] LT',
             nextDay : '[Tomorrow at] LT',
             nextWeek : 'dddd[ next at] LT',
             lastDay : '[Yesterday at] LT',
             lastWeek : '[Last] dddd[ at] LT',
             sameElse : 'L'
         },
         relativeTime : {
             future : 'in %s',
             past : '%s ago',
             s : 'a few seconds',
             ss : '%d seconds',
             m : '1 minute',
             mm : '%d minutes',
             h : '1 hour',
             hh : '%d hours',
             d : '1 day',
             dd : '%d days',
             M : '1 month',
             MM : '%d months',
             y : '1 year',
             yy : '%d years'
         }
     });

     return th;

 })));
