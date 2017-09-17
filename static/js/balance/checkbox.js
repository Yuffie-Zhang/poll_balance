/**
 * Created by yz on 9/15/17.
 */
$(document).ready(function () {
    $(".check_box").change(function () {
        if (this.checked) {
            // the checkbox is now checked
            $(".balance_by").append($(this).attr("value") + ", ");
        }
        else {
            // the checkbox is now unchecked
            var todelete = $(this).attr("value") + ", ";
            $(".balance_by").text(function (i, txt) {
                return txt.replace(todelete, '');
            });
        }
    });

});
