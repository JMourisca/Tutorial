/**
 * Created by juliana on 16/01/16.
 */
app.service("Data", ["$http", function ($http) {
    var obj = {};

    obj.get = function (q, cache) {
        cache = cache || false;
        return $http.get(q, {cache: cache}).then(function (results) {
            return results.data;
        });
    };
    obj.post = function (q, object) {
        return $http.post(q, object).then(function (results) {
            return results.data;
        });
    };
    obj.put = function (q, object) {
        return $http.put(q, object).then(function (results) {
            return results.data;
        });
    };
    obj.delete = function (q) {
        return $http.delete(q).then(function (results) {
            return results.data;
        });
    };

    return obj;
}]).controller("CategoryController", ["Data", "$window", function (Data, $window) {
    var cat = this;

    cat.delete = function(type, id){
        Data.delete("/" + type + "/" + id).then(function (response) {
            if(response.result === "True") {
                console.log(response);
                 $window.location.reload();
            } else {
                console.log(response.msg);
            }
        });
    };
}]);